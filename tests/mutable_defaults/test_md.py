import ast

from pyrid.mutable_defaults.md import has_mutable_default


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


def test_has_mutable_default_list():
    assert has_mutable_default(
        _make_func([ast.List(elts=[ast.Constant(value=1)])])
    ) == ["List"]


def test_has_mutable_default_dict():
    assert has_mutable_default(
        _make_func(
            [ast.Dict(keys=[ast.Constant(value=1)], values=[ast.Constant(value=2)])]
        )
    ) == ["Dict"]


def test_has_mutable_default_set():
    assert has_mutable_default(_make_func([ast.Set(elts=[ast.Constant(value=1)])])) == [
        "Set"
    ]


def test_has_mutable_default_tuple():
    assert (
        has_mutable_default(
            _make_func([ast.Tuple(elts=[ast.Constant(value=1)], ctx=ast.Load())])
        )
        == []
    )
