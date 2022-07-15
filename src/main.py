from .parser import Parser


def main():
    testfile = "./test_file.md"
    p = Parser(testfile)
    p.parse()
    for line in p.retrieve_todos():
        print(line)


if __name__ == "__main__":
    main()
