run:
	PYTHONPATH=src uv run python -m data_validation_tool.main

format:
	uv run black .

install:
	uv sync