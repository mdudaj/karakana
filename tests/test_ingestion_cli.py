from typer.testing import CliRunner

from karakana.cli import app


def test_ingest_file_review_apply_and_list_cli(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("architecture decision command\n", encoding="utf-8")

    result = CliRunner().invoke(app, ["ingest", "file", "README.md", "--project", "karakana", "--classify"])

    assert result.exit_code == 0
    assert "Ingest ID:" in result.output
    ingest_id = [line.split(":", 1)[1].strip() for line in result.output.splitlines() if line.startswith("Ingest ID:")][0]

    review = CliRunner().invoke(app, ["ingest", "review", ingest_id])
    assert review.exit_code == 0
    assert "Status:" in review.output

    apply = CliRunner().invoke(app, ["ingest", "apply", ingest_id])
    assert apply.exit_code == 0
    assert "Dry run" in apply.output

    listed = CliRunner().invoke(app, ["ingest", "list"])
    assert listed.exit_code == 0
    assert ingest_id in listed.output
