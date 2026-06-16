from pyrid.config import load_config


def test_load_config_empty_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text("")
    assert load_config() == {}


def test_load_config_missing_lint_section(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text("[tool.pyrid]\n")
    assert load_config() == {}


def test_load_config_with_lint_section(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    toml_content = """
        [tool.pyrid.lint]
        rules = ["E123", "W456"]
    """
    (tmp_path / "pyproject.toml").write_text(toml_content)
    expected = {"rules": ["E123", "W456"]}
    assert load_config() == expected
