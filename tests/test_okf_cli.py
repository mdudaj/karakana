from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app


def test_okf_validate_cli_passes_for_repository_bundle():
    result = CliRunner().invoke(app, ["okf", "validate"])

    assert result.exit_code == 0
    assert "OKF validation: passed" in result.output
    assert "Concepts by type:" in result.output
    assert "Concepts by project:" in result.output
    assert "karakana" in result.output
    assert "msc-platform" in result.output


def test_okf_validate_cli_accepts_explicit_file():
    result = CliRunner().invoke(app, ["okf", "validate", "okf/karakana/project.md"])

    assert result.exit_code == 0
    assert "Concepts: 1" in result.output
    assert "Project: 1" in result.output


def test_okf_context_cli_previews_selected_concepts():
    result = CliRunner().invoke(
        app,
        ["okf", "context", "--project", "karakana", "--tag", "okf", "--depth", "0", "--limit", "3"],
    )

    assert result.exit_code == 0
    assert "OKF concepts:" in result.output
    assert "karakana.okf.adr" in result.output
    assert "source:" in result.output


def test_okf_scan_promotions_cli_reports_eligible_adr():
    result = CliRunner().invoke(
        app,
        ["okf", "scan-promotions", "docs/adr/0003-okf-entry-point-and-promotion-agent.md", "--eligible-only"],
    )

    assert result.exit_code == 0
    assert "eligible: docs/adr/0003-okf-entry-point-and-promotion-agent.md -> ADR" in result.output


def test_okf_propose_cli_writes_reviewable_proposal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    adr = Path("docs/adr")
    adr.mkdir(parents=True)
    (adr / "0001-demo.md").write_text("# ADR\n", encoding="utf-8")

    result = CliRunner().invoke(
        app,
        ["okf", "propose", "--from", "docs/adr/0001-demo.md", "--reviewer", "test-reviewer"],
    )

    assert result.exit_code == 0, result.output
    assert "OKF proposal written:" in result.output
    assert "Concept draft:" in result.output
    assert "Promotion record:" in result.output
