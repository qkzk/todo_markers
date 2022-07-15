"""
yaml
marked:
    filename1:
    - 12: 
        - issue: 12 
        - content: todo content
    - 23: 
        - issue: 13
        - content: content
    filename2
    - 3: 
        - issue: 14
        - content: content

unmarked:
    filename3:
    - 14:
        -content: content
"""
import yaml


class Editor:
    def __init__(self, path: str, todolist: list) -> None:
        self._path = path
        self._todolist = todolist
