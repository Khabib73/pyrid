from pyrid.colors import green, red, yellow
from pyrid.types import Violation


def format_violation(v: Violation) -> str:
    """Format a single violation into a human-readable form.

    Format::

        <path>:<line>:<column>: <code> <message> - name: <node_name>
    """
    name = ""
    if v.node and hasattr(v.node, "name"):
        name = f" - name: {green(v.node.name)}"

    return f"{red(v.code)} {v.message} in {yellow(v.path)}:{v.line}:{v.column}{name}"


def format_violations(violations: list[Violation]) -> str:
    """Format a list of violations.

    Expects a pre-sorted list. Returns a string with newline separators.
    """
    return "\n".join(format_violation(v) for v in violations)
