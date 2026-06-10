import json

from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_patch_gate_creates_trace(tmp_path, monkeypatch):
    patch_root = tmp_path / ".karakana" / "patches" / "patch"
    patch_root.mkdir(parents=True)
    (patch_root / "changes.diff").write_text("", encoding="utf-8")
    (patch_root / "patch.json").write_text(
        json.dumps({"patch_run_id": "patch", "source_task_id": None, "created_at": "", "git_branch": "feature", "git_status": "", "diff_path": str(patch_root / "changes.diff"), "summary_path": "", "tests_path": None, "files_changed": [], "warnings": [], "errors": []}),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["patch", "gate", "--patch-run", "patch"])
    trace = TraceStore(tmp_path).latest()

    assert result.exit_code == 0
    assert trace.command == "patch gate"
    assert trace.outputs["patch_run_id"] == "patch"
