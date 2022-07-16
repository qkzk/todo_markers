import yaml

from ..api import GithubApi
from ..todo import Todo, get_dumper


class Editor:
    def __init__(self, path: str) -> None:
        self._path = path
        self._current_content = self.load()
        self._todos: dict[str, dict[int, Todo]]
        self.generate_todos()

    def generate_todos(self) -> None:
        self._todos = {
            filepath: {
                linenr: Todo.from_yaml(linenr, content)
                for linenr, content in filecontent.items()
            }
            for filepath, filecontent in self._current_content.items()
        }

    def load(self) -> dict:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError:
            return {}

    def update(self, tododict: dict[str, dict[int, Todo]]):
        self._todos.update(tododict)

    @property
    def todos(self) -> dict[str, dict[int, Todo]]:
        return self._todos

    def write(self):
        yaml.Dumper.ignore_aliases = lambda *args: True
        # print(self._todos)
        # for k, v in self._todos.items():
        #     for todo in v.values():
        #         print(id(todo), todo)
        with open(self._path, "w", encoding="utf-8") as f:
            f.write(yaml.dump(self._todos, Dumper=get_dumper()))
        self._update_files()

    def _update_files(self):
        for filepath, tododict in self._todos.items():
            for line_number, todo in tododict.items():
                self._update_source_file(filepath, line_number, todo)

    def _update_source_file(self, filepath: str, line_number: int, todo: Todo):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not repr(todo) in lines[line_number]:
            lines[line_number] = lines[line_number].replace(todo.todo, repr(todo))
            print(
                f"updated {filepath}, line: {line_number}\ncontent: {lines[line_number]}"
            )
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def publish(self):
        for filename, todos in self._todos.items():
            for linenr, todo in todos.items():
                if todo.has_id():
                    continue
                print(f"posting issue for {filename}, {todo}, {linenr}")
                issue_number = GithubApi("qkzk", "todo_markers").create_issue(todo)
                if issue_number > 0:
                    todo.github_id = issue_number
                break
            break
