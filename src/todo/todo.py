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
        self._updated = False

    @staticmethod
    def _parse_content(line_content: str) -> str:
        return line_content.split(REGEXTODO)[1].splitlines()[0].strip()

    @classmethod
    def from_span(cls, linenr: int, line_content: str) -> Todo:
        todo_line = cls._parse_content(line_content)
        return cls.from_yaml(linenr, todo_line)
        # search = cls._PATTERN.search(todo_line)
        # if search is not None:
        #     todo_id = int(search.group(0)[1:])
        #     _, todo_content = cls._PATTERN.split(todo_line)
        # else:
        #     todo_id = None
        #     todo_content = todo_line
        #
        # todo = cls(linenr, todo_content)
        # if todo_id is not None:
        #     todo.github_id = todo_id
        # return todo
        # todo = cls._parse_content(line_content)

        # return cls(linenr, todo)

    @classmethod
    def from_yaml(cls, linenr_str: str | int, line_content: str) -> Todo:
        search = cls._PATTERN.search(line_content)
        if search is not None:
            todo_id = int(search.group(0)[1:])
            _, todo_content = cls._PATTERN.split(line_content)
        else:
            todo_id = None
            todo_content = line_content

        todo = cls(int(linenr_str), todo_content)
        if todo_id is not None:
            todo.github_id = todo_id

        return todo

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
