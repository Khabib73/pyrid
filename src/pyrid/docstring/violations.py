import ast

from pyrid.types import FuncNode, Violation


def make_d100_violation(node: ast.Module, path: str) -> Violation:
    return Violation(
        code="D100",
        message="Module is missing a docstring",
        path=path,
        line=getattr(node, "lineno", 0),
        column=getattr(node, "col_offset", 0),
        node=node,
    )


def make_d101_violation(node: ast.ClassDef, path: str) -> Violation:
    return Violation(
        code="D101",
        message="Public class is missing a docstring",
        path=path,
        line=getattr(node, "lineno", 0),
        column=getattr(node, "col_offset", 0),
        node=node,
    )


def make_d102_violation(node: FuncNode, path: str) -> Violation:
    return Violation(
        code="D102",
        message="Public method is missing a docstring",
        path=path,
        line=getattr(node, "lineno", 0),
        column=getattr(node, "col_offset", 0),
        node=node,
    )


def make_d103_violation(node: FuncNode, path: str) -> Violation:
    return Violation(
        code="D103",
        message="Public function is missing a docstring",
        path=path,
        line=getattr(node, "lineno", 0),
        column=getattr(node, "col_offset", 0),
        node=node,
    )
