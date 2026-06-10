import json
import subprocess

from karakana.codex.patch import PatchCapture
from karakana.codex.reviewer import PatchReviewer
from karakana.patch.apply import apply_patch_run


def init_repo(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    (tmp_path / "README.md").write_text("old\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True, capture_output=True)


def test_patch_apply_dry_run_uses_check(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "README.md").write_text("new\n", encoding="utf-8")
    artifact = PatchCapture(tmp_path).capture_diff()
    subprocess.run(["git", "checkout", "--", "README.md"], cwd=tmp_path, check=True)
    PatchReviewer(tmp_path).review_diff(tmp_path / ".karakana" / "patches" / artifact.patch_run_id / "changes.diff")

    result = apply_patch_run(tmp_path, artifact.patch_run_id)

    assert result.status == "dry_run_passed"
    assert result.applied is False


def test_patch_apply_refuses_high_risk_write_without_override(tmp_path):
    init_repo(tmp_path)
    path = tmp_path / "billing.py"
    path.write_text("payment = True\n", encoding="utf-8")
    artifact = PatchCapture(tmp_path).capture_diff()
    path.unlink()
    PatchReviewer(tmp_path).review_diff(tmp_path / ".karakana" / "patches" / artifact.patch_run_id / "changes.diff")
    test_root = tmp_path / ".karakana" / "test-runs" / "test"
    test_root.mkdir(parents=True)
    (test_root / "result.json").write_text(json.dumps({"exit_code": 0, "refused": False}), encoding="utf-8")
    from karakana.patch.gates import attach_test_evidence

    attach_test_evidence(tmp_path, artifact.patch_run_id, "test")

    result = apply_patch_run(tmp_path, artifact.patch_run_id, write=True)

    assert result.status == "blocked"
    assert "high-risk patch requires --allow-high-risk" in result.errors
