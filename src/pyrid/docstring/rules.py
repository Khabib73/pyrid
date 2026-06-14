import ast

from pyrid.types import FuncNode


def check_d100(tree: ast.Module) -> bool:
    """
    Check that the module has a docstring.

    Args:
        tree: The AST tree.
    Returns:
        bool: True if the module has a docstring, False otherwise.
    """
    if not tree.body:
        return True
    return bool(ast.get_docstring(tree))


def check_d101(node: ast.ClassDef) -> bool:
    """
    Check that the class has a docstring.

    Args:
        node: The class node to check.
    Returns:
        bool: True if the class has a docstring, False otherwise.
    """
    return bool(ast.get_docstring(node))


def check_d102(node: FuncNode) -> bool:
    """
    Check that the function has a docstring.

    Args:
        node: The function node to check.
    Returns:
        bool: True if the function has a docstring, False otherwise.
    """
    return bool(ast.get_docstring(node))


def check_d103(node: FuncNode) -> bool:
    """
    Check that the class method has a docstring.

    Args:
        node: The function node to check.
    Returns:
        bool: True if the class method has a docstring, False otherwise.
    """
    return bool(ast.get_docstring(node))
