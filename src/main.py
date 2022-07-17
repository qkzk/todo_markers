from .arguments import argument_parser, read_args
from .editor import Editor
from .explorer import Explorer
from .parser import Parser


def main():
    rootdir, export_file, verbose = read_args(argument_parser())
    print(f"exploring from {rootdir}, exporting to {export_file}")
    explorer = Explorer(rootdir)
    explorer.explore()
    editor = Editor(export_file, explorer.todos, verbose)
    editor.todos = explorer.todos
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
