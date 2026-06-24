import subprocess

from karakana.codex.patch import PatchCapture


def test_patch_capture_with_no_diff(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)

    artifact = PatchCapture(tmp_path).capture_diff()

    assert artifact.diff_path
    assert "No working tree changes detected." in artifact.warnings


def test_patch_capture_with_working_tree_diff(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "tests@example.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Karakana Tests"], cwd=tmp_path, check=True)
    path = tmp_path / "README.md"
    path.write_text("old\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True, capture_output=True)
    path.write_text("new\n", encoding="utf-8")

    artifact = PatchCapture(tmp_path).capture_diff()

    assert "README.md" in artifact.files_changed
    assert "new" in (tmp_path / ".karakana" / "patches" / artifact.patch_run_id / "changes.diff").read_text(encoding="utf-8")


def test_patch_capture_records_project_scope(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)

    artifact = PatchCapture(tmp_path).capture_diff(project="demo", skillpack="demo-pack")

    assert artifact.project == "demo"
    assert artifact.skillpack == "demo-pack"
    assert artifact.repository_path == str(tmp_path.resolve())
