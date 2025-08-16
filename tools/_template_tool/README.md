# Template Tool

Use this as a starting point for new dkdevtools tools.

## How to copy

- Duplicate this folder and rename it (e.g., `my_cool_tool`).
- Update `pyproject.toml` project name, description, and scripts.
- Rename the Python package under `src/template_tool` to your tool's package name.
- Search and replace `template_tool` references.

## Dev

- Install: `pip install -e .[dev]` (add extras if you define them)
- Run tests: `pytest`
- Lint/format: `ruff check .` and `ruff format .`
