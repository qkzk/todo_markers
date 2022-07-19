"""
TodoMarkers: Explore a folder looking for todo comments.
Any kind of TODO: #41 - blablabla will be reported in a common file.
"""
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
    parser.add_argument(
        "-v",
        "--verbose",
        help="Display read, write and API informations",
        required=False,
        action="store_true",
    )
    args = parser.parse_args()
    return args


def read_args(args: argparse.Namespace) -> tuple[str, str, bool]:
    args = argument_parser()
    rootdir = args.rootdir
    file = args.export_file
    verbose = args.verbose
    if file is None:
        file = EXPORT_FILE
    export_file = os.path.join(rootdir, file)
    return rootdir, export_file, verbose
