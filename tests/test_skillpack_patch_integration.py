import json

from karakana.patch.gates import run_patch_gate
from karakana.skillpacks.resolver import SkillpackResolver


def test_patch_gate_uses_skillpack_blocked_path(tmp_path):
    patch_root = tmp_path / ".karakana" / "patches" / "patch"
    patch_root.mkdir(parents=True)
    diff = "diff --git a/secrets/key.txt b/secrets/key.txt\n+++ b/secrets/key.txt\n@@\n+value\n"
    (patch_root / "changes.diff").write_text(diff, encoding="utf-8")
    (patch_root / "patch.json").write_text(
        json.dumps({"patch_run_id": "patch", "source_task_id": None, "created_at": "", "git_branch": "feature", "git_status": "", "diff_path": str(patch_root / "changes.diff"), "summary_path": "", "tests_path": None, "files_changed": ["secrets/key.txt"], "warnings": [], "errors": []}),
        encoding="utf-8",
    )
    context = SkillpackResolver(__import__("pathlib").Path.cwd()).resolve_for_project("nhrdm")

    gate, _ = run_patch_gate(tmp_path, "patch", skillpack_context=context)

    assert gate.blocked
    assert "skillpack_blocked_path" in gate.metadata["blocking_signals"]
