import os


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
