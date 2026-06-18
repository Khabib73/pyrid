import ast

import pytest

from pyrid.docstring.rules import check_d100, check_d101, check_d103


def _make_module(docstring: str | None = None) -> ast.Module:
    body = (
        [ast.Expr(value=ast.Constant(value=docstring))] if docstring else [ast.Pass()]
    )
    return ast.Module(body=body, type_ignores=[])


def _make_func(docstring: str | None = None):

    body = (
        [ast.Expr(value=ast.Constant(value=docstring)), ast.Pass()]
        if docstring
        else [ast.Pass()]
    )

    return ast.FunctionDef(
        name="foo",
        args=ast.arguments(
            args=[],
            kwonlyargs=[],
            defaults=[],
        ),
        body=body,
    )


def _make_async_func(docstring: str | None = None):

    body = (
        [ast.Expr(value=ast.Constant(value=docstring)), ast.Pass()]
        if docstring
        else [ast.Pass()]
    )

    return ast.AsyncFunctionDef(
        name="foo",
        args=ast.arguments(
            args=[],
            kwonlyargs=[],
            defaults=[],
        ),
        body=body,
    )


def _make_class(docstring: str | None = None):

    body = (
        [ast.Expr(value=ast.Constant(value=docstring)), ast.Pass()]
        if docstring
        else [ast.Pass()]
    )

    return ast.ClassDef(
        name="Foo",
        body=body,
    )


@pytest.mark.parametrize(
    "module, expected",
    [
        (_make_module(), False),
        (_make_module("Module docstring"), True),
        (_make_module("""Multi-line\n docstring"""), True),
    ],
)
def test_check_d100(module, expected):
    assert check_d100(module) is expected


def test_check_d100_empty_module():
    module = ast.Module(body=[], type_ignores=[])
    assert check_d100(module) is True


@pytest.mark.parametrize(
    "cls, expected", [(_make_class(), False), (_make_class("foo"), True)]
)
def test_check_d101(cls, expected):
    assert check_d101(cls) is expected


@pytest.mark.parametrize(
    "cls, expected", [(_make_func(), False), (_make_func("foo"), True)]
)
def test_check_d103(cls, expected):
    assert check_d103(cls) is expected


@pytest.mark.parametrize(
    "cls, expected", [(_make_async_func(), False), (_make_async_func("foo"), True)]
)
def test_check_d103_async(cls, expected):
    assert check_d103(cls) is expected
