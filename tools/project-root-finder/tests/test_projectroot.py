from pathlib import Path

from projectroot import find_project_root


def test_find_project_root_with_git(tmp_path: Path):
    """Test finding project root with .git marker."""
    project = tmp_path / "test_project" 
    project.mkdir()
    (project / ".git").mkdir()
    
    nested = project / "src" / "deep" / "path"
    nested.mkdir(parents=True)
    
    root = find_project_root(nested)
    assert root == project


def test_find_project_root_not_found(tmp_path: Path):
    """Test when no project root is found."""
    empty = tmp_path / "empty"
    empty.mkdir()
    
    root = find_project_root(empty)
    assert root is None
