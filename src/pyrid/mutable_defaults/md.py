import ast

from pyrid.enums import MutableType
from pyrid.utils import format_mutable_msg

AST_MUTABLE_TYPES = (
    ast.List,
    ast.Dict,
    ast.Set,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
)


def is_mutable_class(node: ast.ClassDef) -> bool:
    """
    Check if a class is mutable.

    A class is considered immutable only if it's a frozen dataclass.

    Args:
        node (ast.ClassDef): The class node.
    Returns:
        bool: True if the class is mutable, False otherwise.
    """

    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call):
            if (
                isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == "dataclass"
            ):
                for keyword in decorator.keywords:
                    if (
                        keyword.arg == "frozen"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value
                    ):
                        return False

            if (
                isinstance(decorator.func, ast.Name)
                and decorator.func.id == "dataclass"
            ):
                for keyword in decorator.keywords:
                    if (
                        keyword.arg == "frozen"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value
                    ):
                        return False

    return True


def has_mutable_default(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    mutable_classes: dict[str, bool] | None = None,
) -> list[str]:
    """
    Check if a function has mutable defaults.

    Args:
        node: The function node to check.
        mutable_classes: Optional dict of class names -> is_mutable.
                         Used to detect user-defined mutable classes.
    Returns:
        list[str]: List of mutable type names found in defaults.
    """
    if mutable_classes is None:
        mutable_classes = {}

    found: list[str] = []

    for arg in node.args.defaults:
        if isinstance(arg, ast.Call):
            if isinstance(arg.func, ast.Attribute) and arg.func.attr in MutableType:
                found.append(arg.func.attr)

            if isinstance(arg.func, ast.Name) and (
                arg.func.id in MutableType or mutable_classes.get(arg.func.id, False)
            ):
                found.append(arg.func.id)

        else:
            for mt in AST_MUTABLE_TYPES:
                if isinstance(arg, mt):
                    found.append(mt.__name__)

    return found


def check_file(tree: ast.Module, path: str = "") -> int:
    """
    Check an entire AST module for mutable defaults.

    Args:
        tree: The AST module to check.
        path: Optional file path for error messages.
    Returns:
        int: The number of errors found.
    """
    errors = 0
    mutable_classes: dict[str, bool] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            mutable_classes[node.name] = is_mutable_class(node)

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found = has_mutable_default(node, mutable_classes)
            for type_name in found:
                print(format_mutable_msg(path, node, type_name, node.name))
                errors += 1

    return errors
