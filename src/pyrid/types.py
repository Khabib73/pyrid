import ast
from dataclasses import dataclass

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
