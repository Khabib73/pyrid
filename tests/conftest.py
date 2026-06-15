import ast

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