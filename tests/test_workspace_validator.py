from pathlib import Path

from karakana.workspaces.loader import WorkspaceLoader
from karakana.workspaces.status import collect_workspace_status
from karakana.workspaces.validator import WorkspaceValidator


def _write_workspace(tmp_path: Path, *, optional: str = "", strict: bool = False) -> None:
    root = tmp_path / "workspaces"
    root.mkdir()
    (root / "example.yml").write_text(
        "name: example\ndescription: Example\nversion: 0.1.0\nstatus: stable\n"
        f"defaults:\n  require_existing_paths: {str(strict).lower()}\n"
        f"projects:\n  - id: absent\n    path: ../absent\n{optional}",
        encoding="utf-8",
    )


def test_workspace_validator_warns_for_missing_default_checkout(tmp_path):
    _write_workspace(tmp_path)
    result = WorkspaceValidator(tmp_path).validate("example")

    assert result.ok
    assert any("Project path does not exist" in warning for warning in result.warnings)


def test_optional_checkout_absence_is_visible_without_a_stale_path_warning(tmp_path):
    _write_workspace(tmp_path, optional="    optional_checkout: true\n")

    result = WorkspaceValidator(tmp_path).validate("example")
    status = collect_workspace_status(tmp_path, WorkspaceLoader(tmp_path).load("example"))

    assert result.ok and result.warnings == []
    assert status.status == "ok"
    assert status.project_statuses[0].path_exists is False
    assert status.warnings == []


def test_strict_workspace_still_rejects_missing_optional_checkout(tmp_path):
    _write_workspace(tmp_path, optional="    optional_checkout: true\n", strict=True)

    result = WorkspaceValidator(tmp_path).validate("example")

    assert not result.ok
    assert any("Project path does not exist" in error for error in result.errors)


def test_optional_checkout_must_be_a_boolean(tmp_path):
    _write_workspace(tmp_path, optional='    optional_checkout: "true"\n')

    result = WorkspaceValidator(tmp_path).validate("example")

    assert not result.ok
    assert any("optional_checkout must be a boolean" in error for error in result.errors)


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
