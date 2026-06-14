import ast


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
