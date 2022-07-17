from __future__ import annotations
import re
from typing import Optional

from .comment_keyword import COMMENT_KEYWORDS
from ..todo import Todo

REGEXISSUE = "^#[0-9]* "
REGEXTODO = "TODO: "


class ParserError(Exception):
    pass


class Parser:
    _PATTERN: re.Pattern = re.compile(REGEXISSUE)

    def __init__(self, path: str) -> None:
        self._path = path
        self._ext = path.split(".")[-1]
        self._pattern = re.compile(REGEXTODO)
        self._start_comment: re.Pattern
        self._end_comment: re.Pattern
        self._read_comment_keywoard()
        self._todos: Optional[dict[int, Todo]] = None
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
        todos: dict[int, Todo] = {}
        in_comment_block = False
        for line_nr, line in enumerate(self._lines):
            if not in_comment_block and self._start_comment.search(line):
                print(
                    f"comment block: {self._start_comment.search(line)}, line_nr: {line_nr}, line: {line}"
                )
                in_comment_block = True
            if in_comment_block:
                matched = self._pattern.search(line)
                if matched:
                    print(f"matched {matched}, line_nr: {line_nr}, line: {line}")
                    todo = self.create_todo(line_nr, line)
                    todos[line_nr] = todo
            if in_comment_block and self._end_comment.search(line):
                print(
                    "end comment: {self._end_comment.search(line)}, line_nr: {line_nr}, line: {line}"
                )
                in_comment_block = False
        self._todos = todos

    @staticmethod
    def _parse_content(line_content: str) -> str:
        return line_content.split(REGEXTODO)[1].splitlines()[0].strip()

    @classmethod
    def _split_id_content(cls, todo_line: str) -> tuple[Optional[int], str]:
        search = cls._PATTERN.search(todo_line)
        if search is not None:
            todo_id = int(search.group(0)[1:])
            _, todo_content = cls._PATTERN.split(todo_line)
        else:
            todo_id = None
            todo_content = todo_line
        return todo_id, todo_content

    @classmethod
    def create_todo(cls, linenr: int, line_content: str) -> Todo:
        # TODO: #51 - simplify constructor, move all this to the parser
        todo_line = cls._parse_content(line_content)
        todo_id, todo_content = cls._split_id_content(todo_line)
        todo = Todo(linenr, todo_content)
        if todo_id is not None:
            todo.github_id = todo_id

        return todo

    @property
    def todos(self) -> dict[int, Todo]:
        if self._todos is None:
            raise ParserError(f"Document {self._path} hasn't been parsed")
        return self._todos
