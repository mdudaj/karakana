import json

from karakana.codex.patch import PatchCapture
from karakana.codex.reviewer import PatchReviewer
from karakana.patch.gates import attach_test_evidence, run_patch_gate


def init_repo(tmp_path):
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    (tmp_path / "README.md").write_text("old\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True, capture_output=True)


def test_patch_gate_pass_docs_patch(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "README.md").write_text("new\n", encoding="utf-8")
    artifact = PatchCapture(tmp_path).capture_diff()
    PatchReviewer(tmp_path).review_diff(tmp_path / ".karakana" / "patches" / artifact.patch_run_id / "changes.diff")

    gate, path = run_patch_gate(tmp_path, artifact.patch_run_id)

    assert path.exists()
    assert gate.blocked is False


def test_patch_review_and_gate_preserve_project_scope(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "README.md").write_text("new\n", encoding="utf-8")
    artifact = PatchCapture(tmp_path).capture_diff(project="demo", skillpack="demo-pack")
    diff = tmp_path / ".karakana" / "patches" / artifact.patch_run_id / "changes.diff"
    review_path = PatchReviewer(tmp_path).review_diff(diff)

    review = json.loads(review_path.read_text(encoding="utf-8"))
    gate, _ = run_patch_gate(tmp_path, artifact.patch_run_id)

    assert review["project"] == "demo"
    assert review["skillpack"] == "demo-pack"
    assert gate.metadata["project"] == "demo"
    assert gate.metadata["skillpack"] == "demo-pack"


def test_patch_gate_blocks_secret(tmp_path):
    init_repo(tmp_path)
    (tmp_path / ".env").write_text("client_secret=abc\n", encoding="utf-8")
    artifact = PatchCapture(tmp_path).capture_diff()
    PatchReviewer(tmp_path).review_diff(tmp_path / ".karakana" / "patches" / artifact.patch_run_id / "changes.diff")

    gate, _ = run_patch_gate(tmp_path, artifact.patch_run_id)

    assert gate.blocked
    assert gate.risk_level == "critical"


def test_attach_test_evidence(tmp_path):
    patch_root = tmp_path / ".karakana" / "patches" / "patch"
    test_root = tmp_path / ".karakana" / "test-runs" / "test"
    patch_root.mkdir(parents=True)
    test_root.mkdir(parents=True)
    (test_root / "result.json").write_text(json.dumps({"exit_code": 0, "refused": False}), encoding="utf-8")

    path = attach_test_evidence(tmp_path, "patch", "test")

    assert path.exists()
    assert json.loads(path.read_text(encoding="utf-8"))["test_run_id"] == "test"
