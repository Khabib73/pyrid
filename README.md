# pyrid — Simple Linter for Python
[![Python](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Khabib73/pyrid?style=social)](https://github.com/Khabib73/pyrid)
[![GitHub contributors](https://img.shields.io/github/contributors/khabib73/pyrid.svg)](https://github.com/khabib73/pyrid/graphs/contributors/)
 ![Downloads](https://static.pepy.tech/badge/pyrid)

## Problem

In Python, the default values of arguments are calculated once, at the time of function definition. If you use a mutable type (for example, [] or {}), then all function calls will share the same object. This can lead to unexpected behavior.

Bad code:

```python
def greet(names: list[str], students = []):  # ← problem!
    for name in names:
        students.append(name)
    return students

print(greet(['John', 'Jane', 'Jack']))  # ['John', 'Jane', 'Jack']
print(greet(['Alex']))                  # ['John', 'Jane', 'Jack', 'Alex'] ← bug!
```

Expected output:

```python
['John', 'Jane', 'Jack']
['Alex']
```

## Installation

```bash
pip install pyrid
```

## Usage

You can run pyrid from the command line:

```bash
pyrid path/to/file.py 
```

You can also run pyrid for directory:

```bash
pyrid path/to/file.py 
```

Project Structure

```
pyrid/
├── src/pyrid/
│   ├── __init__.py
│   ├── __main__.py       # CLI entry point
│   ├── colors.py         # Terminal colors
│   ├── enums.py          # MutableType enum
│   ├── utils.py          # File search, formatting
│   └── mutable_defaults/
│       ├── __init__.py
│       ├── md.py         # logic for mutable defaults
│       └── utils.py # utils for mutable defaults
├── tests/
├── pyproject.toml
├── Makefile
└── COMMIT_CONVENTIONS.md
```

### Project uses Github Actions for CI/CD:

- ruff for linting
- ruff for formatting
- pytest for testing
