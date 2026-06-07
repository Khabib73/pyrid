import pytest

from pyrid.utils import search_files


def test_search_files_single_py_file(tmp_path):
    py_file = tmp_path / "module.py"
    py_file.write_text("print('hello')")

    result = search_files(str(py_file))

    assert result == [str(py_file)]


def test_search_files_directory_with_py_files(tmp_path):
    (tmp_path / "app.py").write_text("")
    (tmp_path / "utils.py").write_text("")
    (tmp_path / "data.txt").write_text("not a python file")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "helper.py").write_text("")

    result = search_files(str(tmp_path))

    result_set = {str(p) for p in result}
    expected = {
        str(tmp_path / "app.py"),
        str(tmp_path / "utils.py"),
        str(tmp_path / "sub" / "helper.py"),
    }

    assert result_set == expected
    assert len(result) == 3


def test_search_files_directory_no_py_files(tmp_path):
    (tmp_path / "readme.md").write_text("# Hello")
    (tmp_path / "data.json").write_text("{}")

    result = search_files(str(tmp_path))

    assert result == []


def test_search_files_nonexistent_path():
    with pytest.raises(ValueError):
        search_files("/nonexistent/path")
