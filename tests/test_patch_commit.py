from karakana.patch.commit import commit_patch_run


def test_patch_commit_dry_run(tmp_path):
    import json
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    patch_root = tmp_path / ".karakana" / "patches" / "patch"
    patch_root.mkdir(parents=True)
    (patch_root / "changes.diff").write_text("", encoding="utf-8")
    (patch_root / "patch.json").write_text(
        json.dumps({"patch_run_id": "patch", "source_task_id": None, "created_at": "", "git_branch": "main", "git_status": "", "diff_path": str(patch_root / "changes.diff"), "summary_path": "", "tests_path": None, "files_changed": [], "warnings": [], "errors": []}),
        encoding="utf-8",
    )

    result = commit_patch_run(tmp_path, "patch", "message")

    assert result.status == "dry_run"
    assert result.committed is False


def test_patch_commit_refuses_empty_message(tmp_path):
    import json
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    patch_root = tmp_path / ".karakana" / "patches" / "patch"
    patch_root.mkdir(parents=True)
    (patch_root / "changes.diff").write_text("", encoding="utf-8")
    (patch_root / "patch.json").write_text(
        json.dumps({"patch_run_id": "patch", "source_task_id": None, "created_at": "", "git_branch": "main", "git_status": "", "diff_path": str(patch_root / "changes.diff"), "summary_path": "", "tests_path": None, "files_changed": [], "warnings": [], "errors": []}),
        encoding="utf-8",
    )

    result = commit_patch_run(tmp_path, "patch", "")

    assert result.status == "blocked"
