# Developer Guide

This repo is a Python monorepo of standalone tools. Each tool lives under `tools/<tool-name>` with its own `pyproject.toml` and `src/` layout. Develop tools independently, test locally, and install individually or as a suite.

## Prerequisites
- Python 3.9+ (3.13 supported)
- PowerShell on Windows (commands below use PowerShell)

## Setup the development environment
1) Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dev tooling
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

3) Install all tools in editable mode (suite)
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-all.txt
```

Tip: VS Code tasks are available under Terminal > Run Task (Lint, Format, Test).

## Repository layout
```
.
├─ pyproject.toml            # Root config (Ruff, pytest); meta only
├─ requirements-dev.txt      # Dev tools (ruff, pytest, hatch, cookiecutter)
├─ requirements-all.txt      # Editable installs for all tools during dev
├─ tools/
│  ├─ _template_tool/        # Copy this to start a new tool
│  └─ dk-sayhi/              # Example tool (CLI)
├─ templates/
│  └─ cookiecutter-dktool/   # Cookiecutter template for new tools
└─ .vscode/                  # Handy tasks/snippets
```

## Add a new tool (Option A: script)
1) Run the scaffolding script (adds optional CLI when --cli provided):
```powershell
.\.venv\Scripts\python.exe .\scripts\new_tool.py "My New Tool" --cli
```
2) Follow on-screen next steps. Also add the tool to the suite for easy dev installs:
```powershell
Add-Content requirements-all.txt "-e tools/my-new-tool"
.\.venv\Scripts\python.exe -m pip install -e tools/my-new-tool
```

VS Code snippet: open a PowerShell file or terminal and type `dk-new-tool` to insert the command.

## Add a new tool (Option B: Cookiecutter)
1) Ensure Cookiecutter is installed (provided by requirements-dev.txt).
2) Generate from template:
```powershell
.\.venv\Scripts\python.exe -m cookiecutter templates/cookiecutter-dktool
```
3) Answer prompts. Then add to the suite and install:
```powershell
Add-Content requirements-all.txt "-e tools/<your-slug>"
.\.venv\Scripts\python.exe -m pip install -e tools/<your-slug>
```

## Test
- Run all tests in the repo:
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
- Run tests for a single tool:
```powershell
.\.venv\Scripts\python.exe -m pytest tools/my-new-tool -q
```

## Lint and format
- Check:
```powershell
.\.venv\Scripts\python.exe -m ruff check .
```
- Auto-fix + format:
```powershell
.\.venv\Scripts\python.exe -m ruff check . --fix
.\.venv\Scripts\python.exe -m ruff format .
```

## Manual testing
- If your tool exposes a CLI via `[project.scripts]`, run it directly after install:
```powershell
# suite install covers all tools listed in requirements-all.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-all.txt
# now call the CLI
my-new-tool --help
```
- Run a module directly:
```powershell
.\.venv\Scripts\python.exe -m my_new_tool.cli --help
```
- Library-style tools, try in REPL:
```powershell
.\.venv\Scripts\python.exe -c "from my_new_tool import hello; print(hello('World'))"
```

## Troubleshooting
- Tests can’t import your package: ensure `tests/conftest.py` exists (from template) and your package dir is under `src/`.
- CLI not found: confirm `[project.scripts]` in the tool’s `pyproject.toml` and reinstall the tool (`pip install -e tools/my-new-tool`).
- Ruff import order issues: run `ruff check . --fix`.
