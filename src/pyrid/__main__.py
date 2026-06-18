import argparse
import ast
import sys

from pyrid.config import load_config
from pyrid.docstring import docstring_checks
from pyrid.rules import resolve_rules
from pyrid.utils import read_code, search_files


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional argument list (defaults to ``sys.argv[1:]``).

    Returns:
        Parsed namespace with ``path``, ``select``, and ``ignore`` attributes.
    """
    parser = argparse.ArgumentParser(
        prog="pyrid",
        description="Simple linter for Python",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to a Python file or directory to lint",
    )
    parser.add_argument(
        "--select",
        nargs="*",
        help="Rules or groups to enable (e.g. D D101)",
    )
    parser.add_argument(
        "--ignore",
        nargs="*",
        help="Rules or groups to disable (e.g. D101)",
    )
    return parser.parse_args(argv)


def main() -> None:

    args = parse_args()
    config = load_config()

    select = args.select or config.get("select")
    ignore = args.ignore or config.get("ignore")

    active_rules = resolve_rules(select, ignore)
    register_checks = [docstring_checks]

    path = args.path
    files = search_files(path)
    errors = 0

    for file in files:
        try:
            tree = ast.parse(read_code(file))
        except SyntaxError:
            print(f"SyntaxError in {file}")
        else:
            for check in register_checks:
                errors += check(tree, file, active_rules)

    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
