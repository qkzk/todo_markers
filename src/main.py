"""
TodoMarkers: Explore a folder looking for todo comments.
Any kind of # TODO: #41 - blablabla will be reported in a common file.
"""
import argparse
import os

from .parser import Parser
from .todolist import Editor
from .explorer import Explorer

EXPORT_FILE = "todofile.yml"


def argument_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rootdir", help="The root directory from where to scan files")
    parser.add_argument(
        "-e",
        "--export_file",
        required=False,
        help=f"The todo export file, default is `rootdir`/{EXPORT_FILE}`",
    )
    args = parser.parse_args()
    return args


def read_args(args: argparse.Namespace) -> tuple[str, str]:
    args = argument_parser()
    rootdir = args.rootdir
    file = args.export_file
    if file is None:
        file = EXPORT_FILE
    export_file = os.path.join(rootdir, file)
    return rootdir, export_file


def main():
    rootdir, export_file = read_args(argument_parser())
    print(f"exploring from {rootdir}, exporting to {export_file}")
    explorer = Explorer(rootdir)
    explorer.explore()
    editor = Editor(export_file)
    editor.load()
    editor.update(explorer.todos)
    editor.publish()
    editor.write()


def test():
    testfile = "src/explorer/explorer.py"
    p = Parser(testfile)
    p.parse()
    print("\nPARSED:")
    for line, todo in p.todos.items():
        print(line, todo)

    explorer = Explorer("./")
    explorer.explore()
    print("\nTODOS FOUND:")
    print(explorer.todos)

    testreport_file = "./test_report.yml"
    editor = Editor(testreport_file)
    report = editor.load()
    # assert report == test_content
    editor.update(explorer.todos)

    print("\n REPORT:")
    print(report)


if __name__ == "__main__":
    main()
