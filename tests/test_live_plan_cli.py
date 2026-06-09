from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from tests.test_model_trace_integration import write_memory_tree, write_skill


def test_plan_live_mock_writes_run_scoped_artifacts(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    write_skill(tmp_path)
    (tmp_path / "KARAKANA.md").write_text("# Contract\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        [
            "plan",
            "--project",
            "karakana",
            "--skill",
            "karakana-self-improvement",
            "--task",
            "Design safer live execution",
            "--live",
            "--provider",
            "mock",
            "--model",
            "mock-model",
        ],
    )

    assert result.exit_code == 0
    assert "Review status:" in result.output
    artifacts = list((tmp_path / ".karakana" / "runs").glob("*/artifacts/model-response.md"))
    assert artifacts
    assert (artifacts[0].parent / "response-review.md").exists()
