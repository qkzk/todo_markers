import os

from ..parser import COMMENT_KEYWORDS
from ..parser import Parser


class Explorer:
    def __init__(self, rootpath: str):
        self._rootpath = os.path.abspath(rootpath)
        print(self._rootpath)
        self._valid_extensions = COMMENT_KEYWORDS.keys()
        self._todos: dict[str, dict[str, str]] = {}

    def explore(self, path=None) -> None:
        if path is None:
            path = self._rootpath
        print(f"path: {path}")
        for f in os.scandir(path):
            if f.is_dir():
                if f.name.startswith(".git"):
                    continue
                self.explore(path=f.path)
            elif f.is_file() and self._is_valid(f.name):
                print(f"file: {f.name}")
                p = Parser(f.path)
                p.parse()
                todos = p.todos
                if todos:
                    self._todos[f.path] = todos

    def _is_valid(self, file: str) -> bool:
        ext = file.split(".")[-1]
        return ext in self._valid_extensions

    @property
    def todos(self) -> dict[str, dict[str, str]]:
        return self._todos


# TODO: que sera ma vie ?
