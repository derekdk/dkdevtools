## Quick orientation for AI coding agents

This repo is a Python monorepo of small, standalone CLI/library tools. Each tool lives under `tools/<tool-slug>` and is a publishable Python project with its own `pyproject.toml` and `src/<package>/` layout. The root project is a meta repo that provides developer tooling and templates.

Keep fixes small and local: prefer editing a single tool under `tools/` unless the change intentionally affects the monorepo metadata (for example, `requirements-all.txt`, root `pyproject.toml`, or tooling in `scripts/`).

## Architecture summary (what to know)
- Monorepo of independent packages: tools are self-contained in `tools/<slug>/` with `pyproject.toml`, `src/` and `tests/`.
- Local dev workflow installs tools in editable mode via `requirements-all.txt` (lines like `-e tools/dk-sayhi`).
- Packaging/build backend: Hatch/Hatchling is used (`build-backend = "hatchling.build"` in `pyproject.toml`).
- CLIs: wired via `[project.scripts]` in each tool's `pyproject.toml`, e.g. `dk-sayhi = "dk_sayhi.cli:main"` which maps to `src/dk_sayhi/cli.py`.

## Project-specific developer workflows (executable examples)
- Set up: create a venv and install dev deps (Windows PowerShell examples in `developer.md`):
  - Create/activate venv: `python -m venv .venv` then `.\\.venv\\Scripts\\Activate.ps1`
  - Install dev tooling: `.\\.venv\\Scripts\\python.exe -m pip install -r requirements-dev.txt`
  - Install all tools (editable): `.\\.venv\\Scripts\\python.exe -m pip install -r requirements-all.txt`
- Tests: repo pytest config restricts tests to `tools/` (see `[tool.pytest.ini_options].testpaths` in root `pyproject.toml`). Run `pytest -q` or target a single tool: `pytest tools/<tool-slug> -q`.
- Lint/format: Ruff is used (root `pyproject.toml` config). Run `ruff check .` and `ruff format .` (see VS Code tasks in `.vscode/tasks.json`).
- Run a tool CLI without installing: `python -m <package>.cli --help` (e.g. `python -m dk_sayhi.cli --help`).

## Scaffolding and templates (how new tools are created)
- Template folder: `tools/_template_tool/` is the scaffold copied by `scripts/new_tool.py`.
- Cookiecutter: `templates/cookiecutter-dktool/` exists for an interactive generator.
- Scripted scaffold: `scripts/new_tool.py` copies the template, renames the package under `src/`, updates text occurrences, and (optionally) adds a CLI and `[project.scripts]` entry when `--cli` is supplied. After scaffold, add `-e tools/<slug>` to `requirements-all.txt` and install.

## Testing conventions and pitfalls
- Each tool includes `tests/conftest.py` that prepends `src/` to `sys.path` so tests run without an editable install. When adding a new tool, ensure a matching `tests/conftest.py` exists or tests will fail to import the package.
- CLI entry points are simple: CLI modules expose `build_parser()` and `main(argv: list[str] | None = None) -> int`. Tests invoke `main([...])` and capture output with `capsys`.

## Linting / style specifics
- Ruff settings live in root `pyproject.toml`: line-length = 100, double-quote preference, and `templates/**` are excluded from linting.
- The repo uses type hints in new code; keep signatures explicit where present.

## Integration points and files to edit for cross-cutting changes
- Add new tool to suite: `requirements-all.txt` (add `-e tools/<your-slug>`).
- Scaffolding behavior: `scripts/new_tool.py` (handles renames and optional CLI injection).
- Cookiecutter hooks: `templates/cookiecutter-dktool/hooks/post_gen_project.py` prints next steps after generation.
- Per-tool packaging/entry points: `tools/<slug>/pyproject.toml`.

## When to change root files
- Change the root `pyproject.toml` only for meta-level changes (pytest config, ruff excludes, packaging metadata). Don't add tool-specific dependencies at the root; edit the tool's `pyproject.toml` instead.

## Example edits the repo expects
- Small bugfix in a single tool: edit `tools/<slug>/src/<pkg>/...` and corresponding `tests/` and run that tool's tests.
- Add CLI: update `tools/<slug>/src/<pkg>/cli.py` and add `[project.scripts]` to that tool's `pyproject.toml`, then reinstall with `pip install -e tools/<slug>` or run `python -m <pkg>.cli` for quick iteration.

## Quick pointers for reviewers/agents
- Prefer minimal, well-scoped PRs that change one tool or the root meta files.
- Run `pytest tools/<slug> -q` and `ruff check <path>` for changed files before proposing a PR.

---
If any part of this file is unclear or you'd like more examples (for example, sample test stubs or a walkthrough of `scripts/new_tool.py`), tell me which section to expand.
