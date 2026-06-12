import ast

import pytest

from pyrid.mutable_defaults import check


def _make_func(defaults: list[ast.expr]) -> ast.FunctionDef:
    """Create a function with the given defaults: def foo(x=default, ...)"""
    return ast.FunctionDef(
        name="foo",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="x")],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=defaults,
        ),
        body=[ast.Pass()],
        decorator_list=[],
    )


def test_has_mutable_default_list_true():
    assert check(
        _make_func([ast.List(elts=[ast.Constant(value=1)])])
    ) == ["List"]


def test_has_mutable_default_dict_true():
    assert check(
        _make_func(
            [ast.Dict(keys=[ast.Constant(value=1)], values=[ast.Constant(value=2)])]
        )
    ) == ["Dict"]


def test_has_mutable_default_set_true():
    assert check(_make_func([ast.Set(elts=[ast.Constant(value=1)])])) == [
        "Set"
    ]


def test_has_mutable_default_tuple_false():
    assert (
        check(
            _make_func([ast.Tuple(elts=[ast.Constant(value=1)], ctx=ast.Load())])
        )
        == []
    )


@pytest.mark.parametrize(
    ("func_name", "expected"),
    [
        ("list", ["list"]),
        ("dict", ["dict"]),
        ("set", ["set"]),
    ],
)
def test_has_mutable_default_call_true(func_name: str, expected: list[str]):
    assert (
        check(
            _make_func([ast.Call(func=ast.Name(id=func_name, ctx=ast.Load()))])
        )
        == expected
    )


def test_has_mutable_default_multiple_calls_true():
    assert check(
        _make_func(
            [
                ast.Call(func=ast.Name(id="set", ctx=ast.Load())),
                ast.Call(func=ast.Name(id="dict", ctx=ast.Load())),
                ast.Call(func=ast.Name(id="list", ctx=ast.Load())),
                ast.Call(func=ast.Name(id="tuple", ctx=ast.Load())),
            ]
        )
    ) == ["set", "dict", "list"]
