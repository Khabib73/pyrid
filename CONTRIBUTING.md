# Contributing to pyrid

Thank you for your interest! We welcome all kinds of contributions – bug reports, feature suggestions, documentation improvements, and code.

<!-- ## Code of Conduct
This project adheres to a [Code of Conduct](link). By participating, you agree to abide by it. -->

## How to Contribute

### Reporting Bugs
- Check the [issue tracker](https://github.com/Khabib73/pyrid/issues) for duplicates.
- If not found, open a new issue.

### Suggesting Enhancements
- Open an issue with the `enhancement` label and describe your idea.

### Your First Code Contribution
- Look for issues labelled `good first issue` or `help wanted`.
- Comment on the issue to let us know you’re working on it.

## Local Development Setup

1. Fork and clone the repo: `git clone https://github.com/Khabib73/pyrid.git`
2. Install dependencies: `poetry install --with dev`
3. Run tests to verify: `make test`

## Submitting Changes

- Create a new branch from `main`: `git checkout -b docs/contribution-guide`.
- Follow [commit conventions](COMMIT_CONVENTIONS.md) (e.g., `feat:`, `fix:`, `docs:`).

- **Ensure code quality checks pass locally** before pushing. We use:
  - **Formatting**: `make format` — automatically formats code with Ruff; `make check_format` only checks formatting without modifying files.
  - **Linting**: `make lint` — runs Ruff to detect code issues (errors, unused imports, style violations). Does not auto-fix.
  - **Type checking**: `make typecheck` — runs mypy to verify static types.
  - **Unit tests**: `make test` — runs the full test suite with pytest.

- Open a Pull Request (PR) to `main`.
- Describe your changes and link any related issues.

## Code Review
All PRs are reviewed by at least one maintainer. We aim to give feedback within 2 business days.

## Questions?
Join our chat on [discussions](https://github.com/Khabib73/pyrid/discussions) in the `#help` category.