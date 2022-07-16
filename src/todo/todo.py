from __future__ import annotations
import re
from typing import Optional, Type

import yaml


REGEXTODO = "TODO: "
REGEXISSUE = "^#[0-9]* "


class Todo:
    _PATTERN: re.Pattern = re.compile(REGEXISSUE)

    def __init__(self, linenr: int, todo: str):
        self._linenr: int = linenr
        self._todo: str = todo
        self._id: Optional[int] = None

    @staticmethod
    def _parse_content(line_content: str) -> str:
        return line_content.split(REGEXTODO)[1].splitlines()[0].strip()

    @classmethod
    def from_span(cls, linenr: int, line_content: str) -> Todo:
        todo = cls._parse_content(line_content)
        return cls(linenr, todo)

    @classmethod
    def from_yaml(cls, linenr_str: str, line_content: str) -> Todo:
        search = cls._PATTERN.search(line_content)
        if search is not None:
            todo_id = int(search.group(0)[1:])
            _, todo_content = cls._PATTERN.split(line_content)
        else:
            todo_id = None
            todo_content = line_content

        todo = cls(int(linenr_str), todo_content)
        if todo_id is not None:
            todo.id = todo_id

        return todo

    def __repr__(self) -> str:
        if self.has_id():
            return f"#{id} - {self._todo}"
        return self._todo

    @property
    def linenr(self) -> int:
        return self._linenr

    @property
    def todo(self) -> str:
        return self._todo

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, idn) -> None:
        self._id = idn

    def has_id(self) -> bool:
        return self._id is not None


def todo_representer(dumper: yaml.SafeDumper, todo: Todo) -> yaml.nodes.ScalarNode:
    return dumper.represent_str(todo.todo)


def get_dumper() -> Type[yaml.SafeDumper]:
    safe_dumper = yaml.SafeDumper
    safe_dumper.add_representer(Todo, todo_representer)
    return safe_dumper
