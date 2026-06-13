from pyrid.colors import green, red, yellow
from pyrid.types import FuncClassNode


def format_docstring_msg(
    path: str,
    node: FuncClassNode,
    func_name: str,
) -> str:
    """
    Args:
        path: The path to the file.
        node: The node to check.
        func_name: The name of the function.
    Returns:
        str: The formatted message.
    """
    return (
        f"{red('Required docstring not found')} in {yellow(path)}:{node.lineno}"
        f"- name: {green(func_name)}"
    )
