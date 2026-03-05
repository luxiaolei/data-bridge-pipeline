.PHONY: test lint format demo

test:
	pytest

lint:
	ruff check src tests
	black --check src tests

format:
	black src tests
	ruff check --fix src tests

demo:
	python -m data_bridge_pipeline.cli doctor --profile profiles/dev.yaml || true
