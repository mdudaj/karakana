from typer.testing import CliRunner

from karakana.cli import app


def test_model_review_cli_writes_artifact(tmp_path, monkeypatch):
    response = tmp_path / ".karakana" / "runs" / "run" / "artifacts" / "model-response.md"
    response.parent.mkdir(parents=True)
    response.write_text("Safe response.\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["model", "review", str(response)])

    assert result.exit_code == 0
    assert "Review status:" in result.output
    assert (response.parent / "response-review.md").exists()


def test_model_review_cli_blocks_unsafe_response(tmp_path, monkeypatch):
    response = tmp_path / ".karakana" / "runs" / "run" / "artifacts" / "model-response.md"
    response.parent.mkdir(parents=True)
    response.write_text("git push origin main\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["model", "review", str(response)])

    assert result.exit_code == 1
    assert "Review status: blocked" in result.output
