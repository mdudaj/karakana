from pathlib import Path

from karakana.workspaces.validator import WorkspaceValidator


def test_workspace_validator_warnings_for_missing_paths():
    result = WorkspaceValidator(Path.cwd()).validate("nimr")

    assert result.ok
    assert any("Project path does not exist" in warning for warning in result.warnings)


def test_workspace_validator_errors_for_duplicate_project_ids(tmp_path):
    root = tmp_path / "workspaces"
    root.mkdir()
    (root / "bad.yml").write_text(
        """name: bad
description: Bad
version: 0.1.0
status: stable
defaults:
  require_existing_paths: true
projects:
  - id: one
    path: missing
  - id: one
    path: missing
""",
        encoding="utf-8",
    )

    result = WorkspaceValidator(tmp_path).validate("bad")

    assert not result.ok
    assert any("Duplicate project id" in error for error in result.errors)
    assert any("Project path does not exist" in error for error in result.errors)
