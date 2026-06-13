import ast

import pytest

from pyrid.docstring.checker import has_docstring


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
    "docstring, expected", [(None, False), ("some docstring", True)]
)
def test_func_has_docstring(docstring, expected):

    func = _make_func(docstring)
    assert has_docstring(func) is expected


@pytest.mark.parametrize(
    "docstring, expected", [(None, False), ("some docstring", True)]
)
def test_async_func_has_docstring(docstring, expected):

    func = _make_async_func(docstring)
    assert has_docstring(func) is expected


@pytest.mark.parametrize(
    "docstring, expected", [(None, False), ("some docstring", True)]
)
def test_class_has_docstring(docstring, expected):

    cls = _make_class(docstring)
    assert has_docstring(cls) is expected
