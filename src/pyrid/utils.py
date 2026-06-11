import ast
import os

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


def search_files(path: str) -> list[str]:
    """
    Args:
        path (str): The path to the file.
    Returns:
        list[str]: The list of files.
    """
    if os.path.isfile(path):
        return [path]
    else:
        res = []
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a file or directory")
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    res.append(os.path.join(root, file))
        return res


def read_code(path: str) -> str:
    """
    Args:
        path (str): The path to the file.
    Returns:
        str: The code.
    """
    with open(path) as f:
        return f.read()
