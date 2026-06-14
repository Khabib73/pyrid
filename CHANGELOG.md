# Changelog

## [Unreleased]

### Added
- Add rule selection system with groups and `pyproject.tool.pyrid.lint` config ([#17])
- Add `docstring` rule: checks that all public functions and classes have a docstring ([#17])
- Add `mutable-defaults` rule: warns when a mutable literal is used as a function default argument
- Add config discovery: read settings from `pyproject.toml` under `[tool.pyrid.lint]` ([#17])
- Add colored terminal output for error messages

### Changed
- Refactor checker architecture to support pluggable rule groups ([#17])

[#17]: https://github.com/Khabib73/pyrid/pull/17

## [0.1.0] - 2023-03-14
### Added
- Initial release


