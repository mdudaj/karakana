import json

from typer.testing import CliRunner

from karakana.cli import app


def test_model_route_cli_output():
    result = CliRunner().invoke(app, ["model", "route", "--task-type", "routine_code_implementation"])

    assert result.exit_code == 0
    assert "Task type: routine_code_implementation" in result.output
    assert "Provider: openai_codex" in result.output
    assert "Model: gpt-5.4-mini" in result.output
    assert "Rationale:" in result.output


def test_model_route_cli_json_output():
    result = CliRunner().invoke(app, ["model", "route", "--task-type", "payment_or_billing_logic", "--json"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["provider"] == "openai_codex"
    assert data["model"] == "gpt-5.5"
    assert data["cost_tier"] == "high"


def test_model_route_cli_escalation_signal():
    result = CliRunner().invoke(
        app,
        [
            "model",
            "route",
            "--task-type",
            "refactoring",
            "--signals",
            "security_or_authentication_change",
        ],
    )

    assert result.exit_code == 0
    assert "Recommended escalation: openai_codex/gpt-5.5" in result.output
