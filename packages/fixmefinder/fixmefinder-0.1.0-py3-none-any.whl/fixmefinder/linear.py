import os
import httpx
from pydantic import BaseModel
from typing import Any, List

# type checker cannot infer the program will exit if the value is None
LINEAR_TEAM_ID: str = os.getenv("LINEAR_TEAM_ID") # type: ignore 
if LINEAR_TEAM_ID is None: # type: ignore
    print("Please set the LINEAR_TEAM_ID environment variable.")
    exit(1)

# type checker cannot infer the program will exit if the value is None
LINEAR_API_KEY: str = os.getenv("LINEAR_API_KEY") # type: ignore 
if LINEAR_API_KEY is None: # type: ignore
    print("Please set the LINEAR_API_KEY environment variable.")
    exit(1)

client = httpx.Client(
    base_url="https://api.linear.app/",
    headers={
        "Authorization": LINEAR_API_KEY,
        "Content-Type": "application/json",
    },
)

class IssueData(BaseModel):
    id: str
    title: str
    identifier: str


class IssueCreateResponse(BaseModel):
    success: bool
    issue: IssueData


class GraphQLResponse(BaseModel):
    data: dict[Any, Any] | None = None
    errors: List[dict[Any, Any]] | None = None

def create_issue(title: str, body: str, team_id: str):
    query = """
    mutation IssueCreate($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue {
          id
          title
          identifier
        }
      }
    }
    """

    variables = {
        "input": {
            "title": title,
            "description": body,
            "teamId": team_id,
        }
    }

    response = client.post(
        "graphql",
        json={"query": query, "variables": variables},
    )

    response.raise_for_status()

    raw = response.json()
    parsed = GraphQLResponse.model_validate(raw)

    if parsed.errors:
        raise RuntimeError(f"GraphQL errors: {parsed.errors}")
    
    assert parsed.data is not None, "GraphQL response data is None"

    issue_create = IssueCreateResponse.model_validate(parsed.data["issueCreate"])
    return issue_create