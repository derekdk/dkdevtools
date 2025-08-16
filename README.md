# dkdevtools

A monorepo of small Python tools that boost developer productivity. Each tool lives in its own folder with an isolated `pyproject.toml`, publishable and installable on its own or installed together during development.

## Layout

```
dkdevtools/
├─ pyproject.toml          # Root config (Ruff, pytest), meta only
├─ requirements-dev.txt    # Dev tooling (ruff, pytest, hatch)
├─ requirements-all.txt    # Easy local install of all tools (editable)
└─ tools/
	 ├─ _template_tool/      # Copy this to start a new tool
	 │  ├─ pyproject.toml
	 │  ├─ README.md
	 │  ├─ src/template_tool/
	 │  │  └─ __init__.py
	 │  └─ tests/
	 │     └─ test_template_tool.py
	 └─ dk-sayhi/            # Example tool to validate the setup
			├─ pyproject.toml
			├─ README.md
			├─ src/dk_sayhi/
			│  ├─ __init__.py
			│  └─ cli.py
			└─ tests/
				 └─ test_sayhi.py
```

## Quickstart (local dev)

1) Create and activate a virtual environment (recommended)

2) From repo root, install dev tools and the example tool:

- Dev tooling
	- `python -m pip install -r requirements-dev.txt`
- All tools in editable mode
	- `python -m pip install -r requirements-all.txt`

3) Run tests

- Entire repo or per tool:
	- `pytest tools/dk-sayhi -q`

4) Try the example CLI

- `dk-sayhi --name Derek`

## Create a new tool

- Copy `tools/_template_tool` to `tools/<your-tool-name>`
- Update `pyproject.toml` (project name, description, entry points)
- Rename the package folder under `src/` and update imports
- Add your CLI (optional) under `src/<pkg>/cli.py` and wire it under `[project.scripts]`
- Add tests in `tests/`
- Add the new tool to `requirements-all.txt` as `-e tools/<your-tool-name>` for easy local install

## Conventions

- PEP 621 `pyproject.toml`
- src/ layout, type hints, Ruff for lint/format
- pytest for tests

## Publishing

Each tool is a standalone package. Build and publish from the tool folder (e.g., with Hatch, Poetry, or `build`). The root project is a meta repo only.
