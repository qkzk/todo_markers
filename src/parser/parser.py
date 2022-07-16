from __future__ import annotations
import re
from typing import Optional

from .comment_keyword import COMMENT_KEYWORDS
from ..todo import Todo, REGEXTODO


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, path: str) -> None:
        self._path = path
        self._ext = path.split(".")[-1]
        self._pattern = re.compile(REGEXTODO)
        self._start_comment: re.Pattern
        self._end_comment: re.Pattern
        self._read_comment_keywoard()
        self._todos: Optional[dict[str, Todo]] = None
        self._lines: list[str]
        self._get_lines_of_path()

    def _read_comment_keywoard(self) -> None:
        _comment_keyword = COMMENT_KEYWORDS.get(self._ext)
        if _comment_keyword is None:
            raise ParserError(f"Unknown extenstion {self._ext} for {self._path}")
        start = " | ".join(kw[0] for kw in _comment_keyword)
        end = " | ".join(kw[1] for kw in _comment_keyword)
        self._start_comment = re.compile(start)
        self._end_comment = re.compile(end)

    def _get_lines_of_path(self) -> None:
        with open(self._path) as filecontent:
            self._lines = filecontent.readlines()

    def parse(self) -> None:
        todos: dict[str, Todo] = {}
        in_comment_block = False
        for line_nr, line in enumerate(self._lines):
            if not in_comment_block and self._start_comment.search(line):
                in_comment_block = True
            if in_comment_block:
                matched = self._pattern.search(line)
                if matched:
                    todo = Todo.from_span(line_nr, line)
                    todos[str(line_nr)] = todo
            if in_comment_block and self._end_comment.search(line):
                self.in_comment_block = False
        self._todos = todos

    @property
    def todos(self) -> dict[str, Todo]:
        if self._todos is None:
            raise ParserError(f"Document {self._path} hasn't been parsed")
        return self._todos
