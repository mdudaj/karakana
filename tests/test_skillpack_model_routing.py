from karakana.models.router import route_model
from karakana.skillpacks.resolver import SkillpackResolver
from typer.testing import CliRunner

from karakana.cli import app


def test_skillpack_routes_override_global():
    context = SkillpackResolver(__import__("pathlib").Path.cwd()).resolve_for_project("nhrdm")
    route = route_model("database_or_index_migration", skillpack_routes=context.model_routes)

    assert route["model"] == "gpt-5.5"
    assert route["route_source"] == "skillpack"


def test_manual_route_override_wins():
    context = SkillpackResolver(__import__("pathlib").Path.cwd()).resolve_for_project("nhrdm")
    route = route_model("database_or_index_migration", provider="mock", model="mock-model", skillpack_routes=context.model_routes)

    assert route["provider"] == "mock"
    assert route["route_source"] == "manual_override"


def test_model_route_cli_accepts_skillpack():
    result = CliRunner().invoke(app, ["model", "route", "--task-type", "database_or_index_migration", "--skillpack", "nhrdm"])

    assert result.exit_code == 0
    assert "Skillpack: nhrdm" in result.output
    assert "Route source: skillpack" in result.output
