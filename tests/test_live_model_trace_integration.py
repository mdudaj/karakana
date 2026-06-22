import json

from typer.testing import CliRunner

from karakana.cli import app
from karakana.traces.store import TraceStore


def test_model_complete_live_trace_records_artifacts_and_redacts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["model", "complete", "--provider", "mock", "--model", "mock-model", "--prompt", "Write a safe summary", "--live"])

    trace = TraceStore(tmp_path).latest()
    assert result.exit_code == 0
    assert trace.outputs["live"] is True
    assert trace.outputs["model_response_artifact"].endswith("model-response.md")
    assert trace.outputs["response_review_artifact"].endswith("response-review.md")
    assert "api_key" not in json.dumps(trace.to_dict()).lower()


def test_model_complete_without_live_is_dry_run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["model", "complete", "--provider", "mock", "--model", "mock-model", "--prompt", "Write a safe summary"])

    trace = TraceStore(tmp_path).latest()
    assert result.exit_code == 0
    assert trace.outputs["dry_run"] is True
    assert not list((tmp_path / ".karakana" / "runs").glob("*/artifacts/model-response.md"))
