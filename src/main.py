from .parser import Parser
from .todolist import Editor
from .explorer import Explorer


def main():
    pass


def test():
    testfile = "src/explorer/explorer.py"
    # p = Parser(testfile)
    # p.parse()
    # print("\nPARSED:")
    # for line, todo in p.todos.items():
    #     print(line, todo)

    explorer = Explorer("./")
    explorer.explore()
    print("\nTODOS FOUND:")
    print(explorer.todos)

    testreport_file = "./test_report.yml"
    editor = Editor(testreport_file, explorer.todos)
    report = editor.load()
    # assert report == test_content
    editor.update()

    print("\n REPORT:")
    print(report)


if __name__ == "__main__":
    main()
