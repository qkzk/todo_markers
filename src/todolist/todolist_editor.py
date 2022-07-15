import yaml


class Editor:
    def __init__(self, path: str, tododict: dict[str, dict[str, str]]) -> None:
        self._path = path
        self._tododict = tododict
        self._current_content = self.load()

    def load(self) -> dict:
        with open(self._path, "r", encoding="utf-8") as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def update(self):
        self._current_content.update(self._tododict)
        print(f"\nnewcontent: {self._current_content}")
        self._write()

    def _write(self):
        with open(self._path, "w", encoding="utf-8") as f:
            yaml.dump(self._current_content, f)
