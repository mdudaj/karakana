from pathlib import Path

from karakana.requirements.prd import generate_prd
from karakana.requirements.schemas import RequirementSource
from karakana.skillpacks.resolver import SkillpackResolver


def test_skillpack_context_adds_skills_tests_and_approvals():
    context = SkillpackResolver(Path.cwd()).resolve_for_project("nhrdm")

    prd = generate_prd(RequirementSource(source_type="note"), "Review custom field OpenSearch migration risk.", skillpack_context=context)

    assert prd.suggested_skillpack == "nhrdm"
    assert "invenio-framework" in prd.suggested_skills
    assert any("Approval required" in item for item in prd.safety_constraints)
