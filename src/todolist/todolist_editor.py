import yaml


class Editor:
    def __init__(self, path: str) -> None:
        self._path = path
        self._current_content = self.load()

    def load(self) -> dict:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError:
            return {}

    def update(self, tododict: dict[str, dict[str, str]]):
        self._current_content.update(tododict)
        self._write()

    @property
    def todos(self) -> dict[str, dict[str, str]]:
        return self._current_content

    def _write(self):
        with open(self._path, "w", encoding="utf-8") as f:
            yaml.dump(self._current_content, f)
