import yaml

from ..api import GithubApi
from ..todo import Todo, get_dumper


class Editor:
    # TODO: #50 - rename file
    def __init__(self, path: str, todos: dict[str, dict[int, Todo]]) -> None:
        self._path = path
        self._todos = todos
        self.to_update: list[tuple[str, Todo]] = []

    def publish(self):
        for filename, todos in self._todos.items():
            for linenr, todo in todos.items():
                if todo.has_id():
                    continue
                print(f"posting issue for {filename}, {todo}, {linenr}")
                issue_number = GithubApi("qkzk", "todo_markers").create_issue(todo)
                if issue_number > 0:
                    todo.github_id = issue_number
                    self.to_update.append((filename, todo))

    def write(self) -> None:
        self._dump_to_yaml()
        self._update_files()

    def _dump_to_yaml(self) -> None:
        yaml.Dumper.ignore_aliases = lambda *args: True
        with open(self._path, "w", encoding="utf-8") as f:
            f.write(yaml.dump(self._todos, Dumper=get_dumper()))

    def _update_files(self) -> None:
        for filepath, todo in self.to_update:
            self._update_source_file(filepath, todo)

    def _update_source_file(self, filepath: str, todo: Todo) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        line_number = todo.linenr
        lines[line_number] = lines[line_number].replace(todo.todo, repr(todo))
        print(f"updated {filepath}, line: {line_number}\ncontent: {lines[line_number]}")
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
