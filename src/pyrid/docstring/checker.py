import ast
from typing import TypeGuard

from pyrid.colors import green, red, yellow
from pyrid.types import FuncClassNode


def format_docstring_msg(
    path: str,
    node: FuncClassNode,
    func_name: str,
) -> str:
    """
    Args:
        path: The path to the file.
        node: The node to check.
        func_name: The name of the function.
    Returns:
        str: The formatted message.
    """
    return (
        f"{red('Required docstring not found')} in {yellow(path)}:{node.lineno}"
        f"- name: {green(func_name)}"
    )


def has_docstring(node: FuncClassNode) -> bool:
    """
    Check if a node has a docstring.

    Args:
        node: The node to check.
    Returns:
        bool: True if the node doesn't have a docstring, False otherwise.
    """
    return ast.get_docstring(node) is None


def is_func_or_class(node: ast.AST) -> TypeGuard[FuncClassNode]:
    """
    Check if a node is a function or class.

    Args:
        node: The node to check.
    Returns:
        bool: True if the node is a FuncClassNode, False otherwise.
    """
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))


def is_missing_docstring(node: ast.AST) -> TypeGuard[FuncClassNode]:
    """
    Args:
        node: The node to check.
    Returns:
        bool: True if the node is a FuncClassNode and doesn't have a docstring,
        False otherwise.
    """
    return is_func_or_class(node) and has_docstring(node)


def docstring_checks(tree: ast.Module, path: str = "") -> int:
    """
    Check an entire AST module for required docstrings.

    Args:
        tree: The AST module to check.
        path: Optional file path for error messages.
    Returns:
        int: The number of errors found.
    """
    errors = 0
    for node in ast.walk(tree):
        if is_missing_docstring(node):
            print(format_docstring_msg(path, node, node.name))
            errors += 1
    return errors
