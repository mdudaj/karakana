from typer.testing import CliRunner

from karakana.cli import app


def test_crosslink_cli_scan_list_show_review_propose_apply():
    runner = CliRunner()

    scan = runner.invoke(app, ["crosslink", "scan", "--workspace", "nimr", "--projects", "billing,lims"])
    assert scan.exit_code == 0
    assert "Crosslink ID:" in scan.output
    crosslink_id = [line.split(":", 1)[1].strip() for line in scan.output.splitlines() if line.startswith("Crosslink ID:")][0]

    listed = runner.invoke(app, ["crosslink", "list"])
    assert listed.exit_code == 0
    assert crosslink_id in listed.output

    shown = runner.invoke(app, ["crosslink", "show", crosslink_id])
    assert shown.exit_code == 0
    assert "# Karakana Cross-Project Knowledge Link" in shown.output

    reviewed = runner.invoke(app, ["crosslink", "review", crosslink_id])
    assert reviewed.exit_code == 0
    assert "Status:" in reviewed.output

    proposed = runner.invoke(app, ["crosslink", "propose", crosslink_id])
    assert proposed.exit_code == 0
    assert "Proposals:" in proposed.output

    applied = runner.invoke(app, ["crosslink", "apply", crosslink_id])
    assert applied.exit_code == 0
    assert "Dry run" in applied.output

