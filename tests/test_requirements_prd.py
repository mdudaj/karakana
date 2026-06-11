from pathlib import Path

from karakana.requirements.prd import generate_prd
from karakana.requirements.schemas import RequirementSource
from karakana.requirements.summary import render_prd
from karakana.skillpacks.resolver import SkillpackResolver


def test_prd_generation_has_required_sections_and_harness_mapping():
    prd = generate_prd(
        RequirementSource(source_type="note", project="karakana", title="Manual note"),
        "Add a safe way to review patch readiness before applying patches. Standards Review and Spec Review should be preserved.",
        project="karakana",
    )
    markdown = render_prd(prd)

    assert prd.model_route["model"] == "gpt-5-mini"
    assert prd.harness_impact.instructions
    assert "## Harness Subsystem Impact" in markdown
    assert "## Standards" in markdown
    assert "## Spec" in markdown
    assert "Acceptance Criteria" in markdown


def test_prd_includes_skillpack_context():
    context = SkillpackResolver(Path.cwd()).resolve_for_project("karakana")

    prd = generate_prd(RequirementSource(source_type="note"), "Add requirements issue decomposition.", skillpack_context=context)

    assert prd.suggested_skillpack == "karakana"
    assert "karakana-self-improvement" in prd.suggested_skills
    assert any("karakana eval run" in item for item in prd.test_and_eval_plan)
