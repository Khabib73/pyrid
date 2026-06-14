import ast

from pyrid.docstring.rules import check_d100, check_d101, check_d102, check_d103
from pyrid.rules import GROUP_MAP

from .utils import format_docstring_msg


class DocstringVisitor(ast.NodeVisitor):
    """
    AST visitor that checks docstring presence on modules, classes, methods,
    and public functions.

    Implements the **Visitor** pattern via `ast.NodeVisitor`. Each AST node
    type of interest gets a `visit_<NodeType>` method, called automatically
    when `visit()` traverses the tree.

    The `in_class` flag acts as a **context switch** between two rules:
      - **D102** (class method must have a docstring) — when `in_class is True`
      - **D103** (public function must have a docstring) — when `in_class is False`

    The `errors` counter accumulates violations. After the full traversal,
    `docstring_checks()` returns this count as the exit code.

    Attributes:
        path: File path being checked (used for error formatting).
        active_rules: Set of rule codes enabled for this run.
        errors: Running count of violations found.
        in_class: Flag — are we currently inside a class definition.
    """

    def __init__(self, path: str, active_rules: set[str]) -> None:
        """
        Args:
            path: Path to the file under inspection.
            active_rules: Set of active rule codes (e.g. {"D100", "D102"}).
                        Rules not in this set are silently skipped.
        """
        self.path = path
        self.active_rules = active_rules
        self.errors = 0
        self.in_class = False

    def visit_Module(self, node: ast.Module) -> None:
        """
        Check **D100**: the top-level module must have a docstring.

        Called when entering the root AST node. After the check, continues
        traversing child nodes via `generic_visit()`.
        """
        if "D100" in self.active_rules and not check_d100(node):
            print(format_docstring_msg(self.path, node, self.path))
            self.errors += 1

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Check **D101**: the class must have a docstring.

        Sets `in_class = True` before descending into the class body so that
        nested `visit_FunctionDef` / `visit_AsyncFunctionDef` calls apply
        **D102** (method) instead of **D103** (function).

        Resets `in_class = False` after the class body has been traversed.
        """
        if "D101" in self.active_rules and not check_d101(node):
            print(format_docstring_msg(self.path, node, node.name))
            self.errors += 1

        self.in_class = True
        self.generic_visit(node)
        self.in_class = False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Check **D102** or **D103** depending on context:

          - `in_class is True`  -> D102 (class method needs a docstring)
          - `in_class is False` -> D103 (public function needs a docstring)

        Handles synchronous functions (`def`).
        """
        if self.in_class:
            if "D102" in self.active_rules and not check_d102(node):
                print(format_docstring_msg(self.path, node, node.name))
                self.errors += 1
        else:
            if "D103" in self.active_rules and not check_d103(node):
                print(format_docstring_msg(self.path, node, node.name))
                self.errors += 1

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """
        Check **D102** or **D103** depending on context.

        Handles asynchronous functions (``async def``).
        Logic is identical to `visit_FunctionDef`.
        """
        if self.in_class:
            if "D102" in self.active_rules and not check_d102(node):
                print(format_docstring_msg(self.path, node, node.name))
                self.errors += 1
        else:
            if "D103" in self.active_rules and not check_d103(node):
                print(format_docstring_msg(self.path, node, node.name))
                self.errors += 1

        self.generic_visit(node)


def docstring_checks(
    tree: ast.Module, path: str = "", active_rules: set[str] | None = None
) -> int:
    """
    Run all docstring checks on an AST module.

    Creates a `DocstringVisitor`, walks the tree, and returns the total
    number of violations found.

    Args:
        tree: Root AST node (`ast.Module`) obtained via `ast.parse()`.
        path: File path used for error message formatting. Defaults to "".
        active_rules: Set of rule codes to check.
                      If `None`, all D-rules from `GROUP_MAP["D"]` are used.

    Returns:
        int: Number of violations found. 0 means everything is clean.

    Example:
        >>> with open("example.py") as f:
        ...     tree = ast.parse(f.read())
        >>> errors = docstring_checks(tree, "example.py")
        >>> print(f"Found {errors} docstring issues")
    """
    if active_rules is None:
        active_rules = GROUP_MAP["D"]
    visitor = DocstringVisitor(path, active_rules)
    visitor.visit(tree)
    return visitor.errors
