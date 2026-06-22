import json

from karakana.patch.status import write_patch_status


def test_patch_status_output(tmp_path):
    patch_root = tmp_path / ".karakana" / "patches" / "patch"
    patch_root.mkdir(parents=True)
    (patch_root / "changes.diff").write_text("", encoding="utf-8")
    (patch_root / "patch.json").write_text(
        json.dumps({"patch_run_id": "patch", "source_task_id": None, "created_at": "", "git_branch": "feature", "git_status": "", "diff_path": str(patch_root / "changes.diff"), "summary_path": "", "tests_path": None, "files_changed": [], "warnings": [], "errors": []}),
        encoding="utf-8",
    )

    path, data = write_patch_status(tmp_path, "patch")

    assert path.exists()
    assert "# Karakana Patch Status" in path.read_text(encoding="utf-8")
    assert data["patch_run_id"] == "patch"
