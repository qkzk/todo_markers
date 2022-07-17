import requests

from ..todo import Todo

STATUS_CODE_OK = 201


def read_token():
    with open("./token", "r", encoding="utf-8") as tokenfile:
        return tokenfile.read().strip()


class GithubApi:
    URL = "https://api.github.com/repos/{owner}/{repo}/issues"
    AUTH_TOKEN = {"Authorization": f"token {read_token()}"}

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
