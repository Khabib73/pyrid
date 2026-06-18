import ast
from collections.abc import Callable
from dataclasses import dataclass, field

type FuncNode = ast.FunctionDef | ast.AsyncFunctionDef
type FuncClassNode = FuncNode | ast.ClassDef


@dataclass
class Violation:
    """Single contract for all linter errors.

    Attributes:
        code: Rule code (e.g. "D101").
        message: Human-readable description of the violation.
        path: File path where the violation was found.
        line: Line number.
        column: Column number.
        node: AST node that triggered the violation (optional).
    """

    code: str
    message: str
    path: str
    line: int
    column: int = 0
    node: ast.AST | None = None


@dataclass
class Rule:
    """Descriptor for a single lint rule.

    Attributes:
        code: Rule code (e.g. ``"D101"``).
        group: Group code (e.g. ``"D"``).
        name: Human-readable name (e.g. ``"missing-class-docstring"``).
        description: Short description of what the rule checks.
    """

    code: str
    group: str
    name: str
    description: str


type NodeCheckFn = Callable[[ast.AST, str, set[str]], Violation | None]
"""Signature for a node-level check function.

Receives the matched AST node, the file path, and the set of active rule
codes.  Return a ``Violation`` if the check fails, or ``None`` if it passes.
"""

type CustomCheckFn = Callable[[ast.Module, str, set[str]], list[Violation]]
"""Signature for a fully custom check function.

Receives the entire module AST, the file path, and the set of active rule
codes.  The function is responsible for its own traversal logic and returns
a (possibly empty) list of ``Violation`` objects.
"""


@dataclass
class NodeRule(Rule):
    """A rule that is applied to every AST node of a given type.

    The framework handles tree traversal — the rule author only provides
    a check function that inspects a single node.

    Attributes:
        node_type: The ``ast.AST`` subclass this rule applies to
                   (e.g. ``ast.FunctionDef``).
        check: Callable ``(node, path, active_rules) -> Violation | None``.
    """

    node_type: type[ast.AST]
    check: NodeCheckFn = field(compare=True)


@dataclass
class CustomRule(Rule):
    """A rule with full control over AST traversal.

    Use this when you need a custom traversal strategy — e.g. ``ast.walk()``,
    token-based analysis, or non-AST checks.  The ``check`` callable receives
    the whole ``ast.Module`` and returns a list of ``Violation``.

    Attributes:
        check: Callable ``(tree, path, active_rules) -> list[Violation]``.
    """

    check: CustomCheckFn = field(compare=False)
