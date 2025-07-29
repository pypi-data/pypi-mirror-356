"""Project PullRequest model class."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from ..client import GraphQLClient
from ..queries import load_query
from .comment import Comment
from .events.event import Event


@dataclass
class PullRequest:
    """Represents a pull request in a GitHub Project (V2)."""

    id: str
    number: int
    title: str
    url: str
    state: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    field_values: List[Dict[str, Any]] = None
    author_login: str = ""
    body: Optional[str] = None
    client: Optional[GraphQLClient] = None
    owner: Optional[str] = None
    repo: Optional[str] = None

    def __post_init__(self):
        """Initialize default values for datetime fields."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.field_values is None:
            self.field_values = []

    @classmethod
    def from_response(
        cls,
        data: Dict[str, Any],
        client: Optional[GraphQLClient] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> "PullRequest":
        """Create a PullRequest instance from API response data.

        Args:
            data (Dict[str, Any]): Raw pull request data from API response
            client (Optional[GraphQLClient]): GraphQL client for API calls
            owner (Optional[str]): Owner of the repository
            repo (Optional[str]): Repository name

        Returns:
            PullRequest: New PullRequest instance
        """
        if "content" in data:  # Project item response
            content = data["content"]
            return cls(
                id=content["id"],
                number=content["number"], 
                title=content["title"],
                url=content["url"],
                state=content["state"],
                created_at=datetime.fromisoformat(
                    content["createdAt"].replace("Z", "+00:00")
                ),
                updated_at=datetime.fromisoformat(
                    content["updatedAt"].replace("Z", "+00:00")
                ),
                author_login=content.get("author", {}).get("login", ""),
                body=None,  # Not included in project responses
                field_values=data.get("fieldValues", {"nodes": []})["nodes"],
                client=client,
                owner=owner,
                repo=repo,
            )
        else:  # PR-specific response or search response
            # For search results it's in ["node"], for direct access in data, for specific queries under repository
            if "node" in data:
                pr_data = data["node"]
            elif "repository" in data:
                pr_data = data["repository"]["pullRequest"]
            else:
                pr_data = data
            
            return cls(
                id=pr_data["id"],
                number=pr_data["number"],
                title=pr_data["title"],
                url=pr_data["url"],
                state=pr_data["state"],
                created_at=datetime.fromisoformat(
                    pr_data["createdAt"].replace("Z", "+00:00")
                ),
                updated_at=datetime.fromisoformat(
                    pr_data["updatedAt"].replace("Z", "+00:00")
                ),
                author_login=pr_data["author"]["login"],
                body=pr_data.get("body"),
                field_values=[],  # Not included in PR responses
                client=client,
                owner=owner,
                repo=repo,
            )

    def get_comments(self, first: int = 20) -> Dict[str, List[Comment]]:
        """Get comments on this pull request.

        Args:
            first (int, optional): Number of comments to fetch per page. Defaults to 20.

        Returns:
            dict: Pull request comments as Comment objects, in "nodes" key

        Raises:
            ValueError: If client, owner or repo are not set
            GraphQLError: On GraphQL operation failures
        """
        if not all([self.client, self.owner, self.repo]):
            raise ValueError("client, owner and repo must be set to fetch comments")

        query = load_query("get_issue_comments")  # PRs use same query structure as issues
        variables = {
            "owner": self.owner,
            "repo": self.repo,
            "number": self.number,
            "first": first,
        }

        response = self.client.execute(query, variables)
        comments_data = response["repository"]["issue"]["comments"]
        comments_data["nodes"] = [
            Comment.from_response(node) for node in comments_data["nodes"]
        ]
        return comments_data
        
    def get(
        self, 
        *,
        client: GraphQLClient, 
        repository: str,
        number: int,
        org: Optional[str] = None,
        username: Optional[str] = None
    ) -> "PullRequest":
        """Get a pull request's details and populate this instance.
        
        Args:
            client (GraphQLClient): GraphQL client for API calls
            repository (str): Repository name
            number (int): Pull request number
            org (Optional[str]): Organization name (if PR is in an org's repo)
            username (Optional[str]): Username (if PR is in a user's repo)
            
        Returns:
            PullRequest: Self with populated properties
            
        Raises:
            ValueError: If neither org nor username is provided
            GraphQLError: On GraphQL operation failures
        """
        if not org and not username:
            raise ValueError("Either org or username must be provided")
            
        owner = org if org else username
        query = load_query("get_pull_request")
        variables = {
            "owner": owner,
            "repo": repository,
            "number": number
        }
        
        response = client.execute(query, variables)
        
        # Use from_response to create a pull request instance with all properties
        pr = PullRequest.from_response(response, client, owner, repository)
        
        # Update this instance's attributes with the fetched data
        self.id = pr.id
        self.number = pr.number
        self.title = pr.title
        self.url = pr.url
        self.state = pr.state
        self.created_at = pr.created_at
        self.updated_at = pr.updated_at
        self.author_login = pr.author_login
        self.body = pr.body
        self.field_values = pr.field_values
        self.client = client
        self.owner = owner
        self.repo = repository
        
        return self
        
    def get_timeline(self, first: int = 20) -> List[Event]:
        """Get timeline events on this pull request.

        Args:
            first (int, optional): Number of events to fetch per page. Defaults to 20.

        Returns:
            List[Event]: Pull request timeline events as Event objects

        Raises:
            ValueError: If client, owner or repo are not set
            GraphQLError: On GraphQL operation failures
        """
        if not all([self.client, self.owner, self.repo]):
            raise ValueError("client, owner and repo must be set to fetch timeline events")

        query = load_query("get_pull_request_timeline")
        variables = {
            "owner": self.owner,
            "repo": self.repo,
            "number": self.number,
            "first": first,
        }

        response = self.client.execute(query, variables)
        timeline_data = response["repository"]["pullRequest"]["timelineItems"]
        nodes = [
            Event.create_from_response(node) for node in timeline_data["nodes"] if Event.create_from_response(node)
        ]
        return nodes