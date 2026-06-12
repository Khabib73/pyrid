import ast

from pyrid.colors import cyan, green, red, yellow


def format_mutable_msg(
    path: str,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    type_name: str,
    func_name: str,
) -> str:
    """
    Args:
        path (str): The path to the file.
        node (ast.AST): The node to format.
        type_name (str): The type name.
        func_name (str): The function name.
    Returns:
        str: The formatted message.
    """
    return (
        f"{red('Mutable default')} in {yellow(path)}:{node.lineno}:{node.col_offset}"
        f" - {cyan(type_name)} in {green(func_name)}"
    )
