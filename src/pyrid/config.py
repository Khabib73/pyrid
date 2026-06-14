import tomllib
from pathlib import Path


def load_toml(path: Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_config() -> dict:
    """
    Load the configuration from pyproject.toml.
    """
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        return {}
    data = load_toml(pyproject)
    return data.get("tool", {}).get("pyrid", {}).get("lint", {})
