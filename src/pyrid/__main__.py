import argparse
import ast
import sys

from pyrid.mutable_defaults import check_file as md_check
from pyrid.utils import read_code, search_files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to directory containing python files",
    )

    args = parser.parse_args()
    path = args.path
    files = search_files(path)
    errors = 0

    for file in files:
        try:
            tree = ast.parse(read_code(file))
            errors += md_check(tree, file)
        except SyntaxError:
            print(f"SyntaxError in {file}")

    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
