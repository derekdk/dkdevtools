from __future__ import annotations

from pathlib import Path

from projectroot.cli import find_project_root, main


def test_find_project_root_current(tmp_path: Path, monkeypatch):
    project = tmp_path / "proj"
    project.mkdir()
    # create marker
    (project / ".git").mkdir()

    # nested directory
    nested = project / "a" / "b"
    nested.mkdir(parents=True)

    # Start from nested path
    root = find_project_root(nested)
    assert root == project


def test_cli_prints_root(tmp_path: Path, capsys):
    project = tmp_path / "proj"
    project.mkdir()
    (project / "pyproject.toml").write_text("[project]\nname='x'\n")

    nested = project / "src" / "x"
    nested.mkdir(parents=True)

    code = main(["--start", str(nested)])
    out = capsys.readouterr().out.strip()
    assert code == 0
    assert out == str(project)


def test_cli_exit_code_when_not_found(tmp_path: Path):
    empty = tmp_path / "empty"
    empty.mkdir()
    code = main(["--start", str(empty), "--quiet"])  # expect not found
    assert code == 1
