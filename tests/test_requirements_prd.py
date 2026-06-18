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


def test_prd_generation_uses_elicitation_prd_seed_sections():
    content = """# Requirements Elicitation Result

## Out of Scope

- Curriculum extraction.
- Topic screening.

## Specification / PRD Seed

Create a reviewable PRD for Slice 1.1: Curriculum Intake Management UX and TIE Source Actions.

Problem: Operators lack a web surface to seed default TIE sources and capture source snapshots.

Goal: Enable staff operators to manage TIE curriculum intake readiness from the web.

Functional requirements:

- Staff operators can seed default Tier 1 TIE sources.
- Staff operators can capture a snapshot with explicit mode choices.

Non-functional requirements:

- Reuse existing service functions and model fields.
- Tests must avoid live network dependency.

Acceptance criteria:

- Repeating seed default sources does not create duplicate rows.
- Non-staff users cannot execute intake actions.

Verification:

- Focused Django tests for apps.curriculum.
"""

    prd = generate_prd(RequirementSource(source_type="file"), content, project="msc-platform")

    assert prd.title == "Slice 1.1: Curriculum Intake Management UX and TIE Source Actions"
    assert prd.problem == "Operators lack a web surface to seed default TIE sources and capture source snapshots."
    assert prd.goal == "Enable staff operators to manage TIE curriculum intake readiness from the web."
    assert "Staff operators can seed default Tier 1 TIE sources." in prd.functional_requirements
    assert "Reuse existing service functions and model fields." in prd.non_functional_requirements
    assert "Curriculum extraction." in prd.non_goals
    assert "Repeating seed default sources does not create duplicate rows." in prd.standards_spec.acceptance_criteria
    assert "Focused Django tests for apps.curriculum." in prd.test_and_eval_plan
