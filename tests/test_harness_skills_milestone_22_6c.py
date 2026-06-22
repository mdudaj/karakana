from pathlib import Path

import yaml

from karakana.evals.loader import EvalLoader
from karakana.skills.validator import SkillValidator


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES = (
    "brainstorm-verbalized-sampling",
    "requirements-elicitation",
    "grill-with-docs",
)


def skill_text(name: str) -> str:
    return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def test_milestone_skills_validate_without_warnings():
    validator = SkillValidator()

    for name in SKILL_NAMES:
        result = validator.validate(ROOT / "skills" / name)
        assert result.errors == [], f"{name}: {result.errors}"
        assert result.warnings == [], f"{name}: {result.warnings}"


def test_brainstorm_skill_defines_distribution_uncertainty_and_decision_rule():
    text = skill_text("brainstorm-verbalized-sampling")

    assert "## Option Distribution" in text
    assert "weights summing to 1.0" in text
    assert "## Uncertainty Flags" in text
    assert "## Decision Rule" in text
    assert "not calibrated" in text
    assert "Sensitivity Analysis" in text


def test_requirements_elicitation_is_grounded_and_uses_verbalized_sampling():
    text = skill_text("requirements-elicitation")

    assert "## Document Grounding" in text
    assert "## Verbalized-Sampling Decision Step" in text
    assert "karakana requirements prd" in text
    assert "--from-file" in text
    assert "Do not generate implementation tasks" in text
    assert "Ready for Specification / PRD?" in text


def test_grill_with_docs_challenges_adrs_scope_evidence_and_verification():
    text = skill_text("grill-with-docs")

    for phrase in ("ADRs", "overbroad scope", "missing evidence", "missing tests", "unsafe defaults"):
        assert phrase in text


def test_msc_platform_requires_new_skills():
    data = yaml.safe_load((ROOT / "skillpacks" / "msc-platform.yml").read_text(encoding="utf-8"))

    required = set(data["skills"]["required"])
    assert set(SKILL_NAMES) <= required


def test_all_other_project_skillpacks_offer_new_skills_as_optional():
    for path in (ROOT / "skillpacks").glob("*.yml"):
        if path.stem == "msc-platform":
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        available = set(data["skills"].get("required", [])) | set(data["skills"].get("optional", []))
        assert set(SKILL_NAMES) <= available, path.name


def test_requirements_skill_is_project_and_artifact_agnostic():
    text = skill_text("requirements-elicitation")

    assert "for any software, research, infrastructure, documentation, operations, or product project" in text
    assert "independent of framework, repository layout, issue tracker" in text
    assert "### Karakana integration" in text


def test_milestone_skill_evals_are_discoverable():
    cases = EvalLoader(ROOT).load_cases(suite="skills")
    ids = {case.id for case in cases}

    assert "brainstorm-verbalized-sampling-option-distribution" in ids
    assert "requirements-elicitation-doc-grounded-pre-prd" in ids
    assert "grill-with-docs-adr-doc-challenge" in ids
