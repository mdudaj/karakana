from pathlib import Path

from karakana.skillpacks.resolver import SkillpackResolver, route_from_skillpack


def test_resolve_for_project():
    context = SkillpackResolver(Path.cwd()).resolve_for_project("nhrdm")

    assert "invenio-framework" in context.required_skills
    assert "site/nhrdm/projects/**" in context.high_risk_paths


def test_skillpack_route_override():
    context = SkillpackResolver(Path.cwd()).resolve_for_project("nhrdm")
    route = route_from_skillpack(context.skillpack, "database_or_index_migration")

    assert route["model"] == "gpt-5.5"
