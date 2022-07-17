import argparse
import os

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
