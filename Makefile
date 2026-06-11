.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: format
format:
	poetry run ruff check --select I --fix .
	poetry run ruff format .

.PHONY: check_format
check_format:
	poetry run ruff format --check .

.PHONY: test
test:
	poetry run pytest .

.PHONY: typecheck
typecheck:
	poetry run mypy src/