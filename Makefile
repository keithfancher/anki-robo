.PHONY: format typecheck

format:
	@# Cannot yet sort imports as part of `format`.
	@# See: https://docs.astral.sh/ruff/formatter/#sorting-imports
	ruff check --select I --fix .
	ruff format .

typecheck:
	mypy robo.py
