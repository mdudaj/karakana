from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.memory.ubongo import REQUIRED_GLOBAL_FILES, REQUIRED_PROJECT_FILES


def write_memory_tree(root: Path, project: str = "karakana") -> None:
    global_root = root / "ubongo" / "global"
    project_root = root / "ubongo" / "projects" / project
    global_root.mkdir(parents=True)
    project_root.mkdir(parents=True)
    for filename in REQUIRED_GLOBAL_FILES:
        (global_root / filename).write_text(f"# {filename}\n\nGlobal guidance.\n", encoding="utf-8")
    for filename in REQUIRED_PROJECT_FILES:
        (project_root / filename).write_text(f"# {filename}\n\nProject guidance.\n", encoding="utf-8")


def test_memory_list_projects_cli(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["memory", "list-projects"])

    assert result.exit_code == 0
    assert "karakana" in result.output


def test_memory_validate_cli_success(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["memory", "validate", "--project", "karakana"])

    assert result.exit_code == 0
    assert "Project 'karakana' memory is complete." in result.output


def test_memory_validate_cli_failure(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    (tmp_path / "ubongo" / "projects" / "karakana" / "open-issues.md").unlink()
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["memory", "validate", "--project", "karakana"])

    assert result.exit_code == 1
    assert "open-issues.md" in result.output


def test_memory_show_cli(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["memory", "show", "--project", "karakana"])

    assert result.exit_code == 0
    assert "# Ubongo Memory: karakana" in result.output
    assert "## Project Memory" in result.output
