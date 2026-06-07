[![Python](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Khabib73/pyrid?style=social)](https://github.com/Khabib73/pyrid)
[![GitHub contributors](https://img.shields.io/github/contributors/khabib73/pyrid.svg)](https://github.com/khabib73/pyrid/graphs/contributors/)
 ![Downloads](https://static.pepy.tech/badge/pyrid)

## Problem

Sometimes we used default mutables types like list, dict, set, etc. in our code.
We want to check if we used default mutables types in our code.

Bad code:

```python
def greet(names: list[str], students = []):

    for name in names:
        students.append(name)
    
    return students
```

So, lets run it:

```python
greet(['John', 'Jane', 'Jack']) # ['John', 'Jane', 'Jack']
greet(['Alex',]) # ['John', 'Jane', 'Jack', 'Alex'] expected ['Alex']
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
