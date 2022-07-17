import subprocess

import yaml

from ..api import GithubApi
from ..todo import Todo, get_dumper


class EditorError(Exception):
    pass


class Editor:
    def __init__(
        self, path: str, todos: dict[str, dict[int, Todo]], verbose: bool
    ) -> None:
        self._path = path
        self._todos = todos
        self._verbose = verbose
        self.to_update: list[tuple[str, Todo]] = []

        self._owner, self._repo = self._get_user_repo()

    @staticmethod
    def _get_user_repo() -> tuple[str, str]:
        output = subprocess.check_output(["git", "remote", "-v"]).decode("utf-8")
        for line in output.splitlines():
            if line.startswith("origin"):
                words = line.split("/")
                owner = words[3]
                domain = words[4]
                repo = domain.split(".")[0]
                return owner, repo
        else:
            raise EditorError(
                "Couldn't parse `git remote -v` correctly. Is this a git repository ?"
            )

    def publish(self):
        for filename, todos in self._todos.items():
            for linenr, todo in todos.items():
                if todo.has_id():
                    continue

                if self._verbose:
                    print(f"posting issue for {filename}, {todo}, {linenr}")
                issue_number = GithubApi(
                    self._owner, self._repo, self._verbose
                ).create_issue(todo)
                if issue_number > 0:
                    todo.github_id = issue_number
                    self.to_update.append((filename, todo))

    def write(self) -> None:
        self._dump_to_yaml()
        self._update_source_files()

    def _dump_to_yaml(self) -> None:
        yaml.Dumper.ignore_aliases = lambda *args: True
        with open(self._path, "w", encoding="utf-8") as f:
            f.write(yaml.dump(self._todos, Dumper=get_dumper()))

    def _update_source_files(self) -> None:
        for filepath, todo in self.to_update:
            self._update_single_source_file(filepath, todo)

    def _update_single_source_file(self, filepath: str, todo: Todo) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        line_number = todo.linenr
        lines[line_number] = lines[line_number].replace(todo.todo, repr(todo))
        if self._verbose:
            print(
                f"updated {filepath}, line: {line_number}\ncontent: {lines[line_number]}"
            )
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
