.PHONY: all format lint typecheck test

all: format typecheck lint

format:
	@# Cannot yet sort imports as part of `format`.
	@# See: https://docs.astral.sh/ruff/formatter/#sorting-imports
	@echo "Formatting all python source files..."
	ruff check --select I --fix .
	ruff format .
	@echo "Done\n"

lint:
	@echo "Linting all python source files..."
	ruff check
	@echo "Done\n"

typecheck:
	@echo "Checking types..."
	mypy ankirobo
	@echo "Done\n"

test:
	pytest
