from __future__ import annotations
import re
from typing import Optional

from .comment_keyword import COMMENT_KEYWORDS

REGEXTODO = "TODO: "


class Position:
    def __init__(self, linenr: int, colstart: int, colend: int):
        self._linenr = linenr
        self._colstart = colstart
        self._colend = colend

    @classmethod
    def from_span(cls, linenr: int, span: tuple[int, int]) -> Position:
        return cls(linenr, *span)

    def __repr__(self) -> str:
        return f"Position({self._linenr}, {self._colstart}, {self._colend})"

    @property
    def linenr(self) -> int:
        return self._linenr


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
        self._positions: Optional[list[Position]] = None
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
        todos = []
        in_comment_block = False
        for line_nr, line in enumerate(self._lines):
            if not in_comment_block and self._start_comment.match(line):
                in_comment_block = True
            if in_comment_block:
                matches = self._pattern.finditer(line)
                for match in matches:
                    todos.append(Position.from_span(line_nr, match.span()))
            if in_comment_block and self._end_comment.match(line):
                self.in_comment_block = False
        self._positions = todos

    @property
    def positions(self) -> list[Position]:
        if self._positions is None:
            raise ParserError(f"Document {self._path} hasn't been parsed")
        return self._positions

    def retrieve_todos(self) -> list[tuple[int, str]]:
        """
        Returns a list of TODO content
        """
        return [(pos.linenr, self._lines[pos.linenr]) for pos in self.positions]
