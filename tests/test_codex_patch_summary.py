import json

from karakana.codex.patch import PatchCapture
from karakana.codex.summary import summarize_patch


def test_patch_summary_generation(tmp_path):
    root = tmp_path / ".karakana" / "patches" / "patch"
    root.mkdir(parents=True)
    (root / "changes.diff").write_text("diff --git a/README.md b/README.md\n+++ b/README.md\n", encoding="utf-8")
    (root / "patch.json").write_text(
        json.dumps(PatchCapture(tmp_path).capture_diff().to_dict()),
        encoding="utf-8",
    )

    summary = summarize_patch(tmp_path, "patch")

    assert summary.exists()
    assert "# Karakana Patch Summary" in summary.read_text(encoding="utf-8")
