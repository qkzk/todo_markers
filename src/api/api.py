"""
Request:
curl
  -X POST
  -H "Accept: application/vnd.github+json"
  -H "Authorization: token <TOKEN>"
  https://api.github.com/repos/OWNER/REPO/issues
  -d '{"title":"Found a bug","body":"I'm having a problem with this.","assignees":["octocat"],"milestone":1,"labels":["bug"]}'


response = {
    "url": "https://api.github.com/repos/qkzk/todo_markers/issues/25",
    "repository_url": "https://api.github.com/repos/qkzk/todo_markers",
    "labels_url": "https://api.github.com/repos/qkzk/todo_markers/issues/25/labels{/nam e}",
    "comments_url": "https://api.github.com/repos/qkzk/todo_markers/issues/25/comments",
    "events_url": "https://api.github.com/repos/qkzk/todo_markers/issues/25/events",
    "html_url": "https://github.com/qkzk/todo_marker s/issues/25",
    "id": 1306829582,
    "node_id": "I_kwDOHqkDac5N5KMO",
    "number": 25,
    "title": "que sera ma vie ?",
    "user": {
        "login": "qkzk",
        "id": 13246170,
        "node_id": "MDQ6VXNlcjEzMjQ2MTcw",
        "avatar_url": "https://avatars.gi thubusercontent.com/u/13246170?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/qkzk",
        "html_url": "https://github.com/qkzk",
        "followers_url": "https://api.github.com/users/qkzk/followers",
        "following_url": "https://api.github.com/users/qkzk/following{/other_user}",
        "gists_url": "https://api.github.com/users/qkzk/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/qkzk/starred{/owner}{/repo}",
        "subscriptions_ur l": "https://api.github.com/users/qkzk/subscriptions",
        "organizations_url": "https://api.github.com/users/qkzk/orgs",
        "repos_url": "https://api.github.com/users/qkzk/repos",
        "events_url": "https://api.github.com/users/q kzk/events{/privacy}",
        "received_events_url": "https://api.github.com/users/qkzk/received_events",
        "type": "User",
        "site_admin": False,
    },
    "labels": [],
    "state": "open",
    "locked": False,
    "assignee": None,
    "assignees": [],
    "milestone": None,
    "comments": 0,
    "created_at": "2022-07-16T14:59:34Z",
    "updated_at": "2022-07-16T14:59:34Z",
    "closed_at": None,
    "author_association": "OWNER",
    "active_lock_reason": None,
    "body": "que sera ma vie ?",
    " closed_by": None,
    "reactions": {
        "url": "https://api.github.com/repos/qkzk/todo_markers/issues/25/reactions",
        "total_count": 0,
        "+1": 0,
        "-1": 0,
        "laugh": 0,
        "hooray": 0,
        "confused": 0,
        "heart": 0,
        "rocket": 0,
        "eyes": 0,
    },
    "timeline_url": "https://api.github.com/repos/qkzk/todo_markers/issues/25/timeline",
    "performed_via_github_app": None,
    "state_reason": None,
}
"""
import requests

from ..todo import Todo

STATUS_CODE_OK = 201


class GithubApi:
    URL = "https://api.github.com/repos/{owner}/{repo}/issues"

    def __init__(self, owner: str, repo: str):
        self._owner = owner
        self._repo = repo

    def create_issue(self, todo: Todo) -> int:
        """
        @param todo: (Todo) a todo to be pushed.
        @return : (int)
            -1 if the issue wasn't created propery,
            -2 if the issue already have an id,
            else the number of the issue.
        """
        if todo.has_id():
            return -2
        url = self.URL.format(owner=self._owner, repo=self._repo)
        body = todo.to_json()
        print(url)
        print(body)
        response = requests.post(
            url=url,
            json=body,
            headers=AUTH_TOKEN,
        )
        print(response.status_code)
        print(response.json())
        if response.status_code == STATUS_CODE_OK:
            return response.json()["number"]
        return -1


def read_token():
    with open("./token", "r", encoding="utf-8") as tokenfile:
        return tokenfile.read().strip()


TOKEN = read_token()
AUTH_TOKEN = {"Authorization": f"token {TOKEN}"}
