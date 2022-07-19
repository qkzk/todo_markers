import requests

from ..todo import Todo
from .token import TOKEN

STATUS_CODE_OK = 201


class GithubApi:
    URL = "https://api.github.com/repos/{owner}/{repo}/issues"
    AUTH_TOKEN = {"Authorization": f"token {TOKEN}"}

    def __init__(self, owner: str, repo: str, verbose: bool):
        self._owner = owner
        self._repo = repo
        self._verbose = verbose

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
        response = requests.post(
            url=url,
            json=body,
            headers=self.AUTH_TOKEN,
        )
        if self._verbose:
            print("Github answered with status code: {response.status_code}")
        if response.status_code == STATUS_CODE_OK:
            if self._verbose:
                print(f"New issue created at {response.json()['html_url']}")
            return response.json()["number"]
        return -1
