import ast

from pyrid.docstring.rules import check_d100, check_d101, check_d102, check_d103

from .utils import format_docstring_msg


class DocstringVisitor(ast.NodeVisitor):
    def __init__(self, path: str, active_rules: set[str]) -> None:
        self.path = path
        self.active_rules = active_rules
        self.errors = 0
        self.in_class = False

    def visit_Module(self, node: ast.Module) -> None:
        """
        Check D100: module has docstring
        """
        if "D100" in self.active_rules and not check_d100(node):
            print(format_docstring_msg(self.path, node, self.path))
            self.errors += 1

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Check D101: class has docstring
        """
        if "D101" in self.active_rules and not check_d101(node):
            print(format_docstring_msg(self.path, node, node.name))
            self.errors += 1

        self.in_class = True
        self.generic_visit(node)
        self.in_class = False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Check D102: function has docstring
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
        Check D102: async function has docstring
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
    Run docstring checks on an AST module.

    Args:
        tree: The AST module to check.
        path: Optional file path for error messages.
        active_rules: Set of rule codes to check.
                    Default to all D rules.
    Returns:
        int: The number of errors found.
    """
    if active_rules is None:
        active_rules = {"D100", "D101", "D102", "D103"}
    visitor = DocstringVisitor(path, active_rules)
    visitor.visit(tree)
    return visitor.errors
