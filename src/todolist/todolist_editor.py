import yaml

from ..todo import Todo, get_dumper


class Editor:
    def __init__(self, path: str) -> None:
        self._path = path
        self._current_content = self.load()
        self._todos: dict[str, dict[str, Todo]]
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

    def update(self, tododict: dict[str, dict[str, Todo]]):
        self._todos.update(tododict)
        self._write()

    @property
    def todos(self) -> dict[str, dict[str, Todo]]:
        return self._todos

    def _write(self):
        yaml.Dumper.ignore_aliases = lambda *args: True
        with open(self._path, "w", encoding="utf-8") as f:
            f.write(yaml.dump(self._todos, Dumper=get_dumper()))
