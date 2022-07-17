from __future__ import annotations
from typing import Optional, Type

import yaml


class Todo:
    def __init__(self, linenr: int, todo: str):
        self._linenr: int = linenr
        self._todo: str = todo
        self._id: Optional[int] = None
        self._updated = False

    def __repr__(self) -> str:
        if self.has_id():
            return f"#{self.github_id} - {self._todo}"
        return self._todo

    @property
    def linenr(self) -> int:
        return self._linenr

    @property
    def todo(self) -> str:
        return self._todo

    @property
    def github_id(self) -> Optional[int]:
        return self._id

    @github_id.setter
    def github_id(self, idn) -> None:
        self._id = idn

    def has_id(self) -> bool:
        return self._id is not None

    def to_json(self) -> dict:
        return {
            "title": f"Todo: {self.todo}",
            "body": f"{self.todo}\n\n\nFrom todo_markers",
            "labels": ["Todo"],
        }

    @property
    def updated(self) -> bool:
        return self._updated

    def update(self) -> None:
        self._updated = True


def todo_representer(dumper: yaml.SafeDumper, todo: Todo) -> yaml.nodes.ScalarNode:
    return dumper.represent_str(repr(todo))


def get_dumper() -> Type[yaml.SafeDumper]:
    safe_dumper = yaml.SafeDumper
    safe_dumper.add_representer(Todo, todo_representer)
    return safe_dumper
