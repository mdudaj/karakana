from pathlib import Path

from karakana.skills.loader import SkillLoader
from karakana.skills.validator import SkillValidator

SKILL_ROOT = Path("skills/viewflow-framework")


def test_viewflow_skill_exists_and_metadata_parses():
    skill = SkillLoader(Path("skills")).load_skill("viewflow-framework")

    assert skill.name == "viewflow-framework"
    assert skill.risk_level == "high"
    assert skill.category == "development"
    assert skill.scope == "bundled"
    assert "viewflow" in skill.activation.keywords
    assert "workflow_state_change" in skill.requires_approval_for


def test_viewflow_skill_validation_passes_without_governance_warnings():
    result = SkillValidator().validate(SKILL_ROOT)

    assert result.is_valid
    assert result.errors == []
    assert "Missing recommended section: ## Quick Reference" not in result.warnings
    assert "Missing recommended section: ## Pitfalls" not in result.warnings
    assert "Missing recommended section: ## Verification" not in result.warnings


def test_viewflow_skill_required_sections_and_concepts_exist():
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

    for section in [
        "# Viewflow Framework Skill",
        "## Purpose",
        "## When to use this skill",
        "## When not to use this skill",
        "## Quick Reference",
        "## Core concepts",
        "## Standard workflow",
        "## Pitfalls",
        "## Verification",
        "## Safety rules",
        "## Required checks",
        "## Output format",
        "## Examples",
    ]:
        assert section in text
    for concept in ["Flow data", "Business data", "Permission and assignment review", "Frontend changes", "Tests"]:
        assert concept in text


def test_viewflow_reference_and_template_files_exist():
    for path in [
        "references/workflow-patterns.md",
        "references/cookbook-map.md",
        "references/frontend-patterns.md",
        "references/permissions.md",
        "references/testing.md",
        "references/migration-notes.md",
        "templates/workflow-design-checklist.md",
        "templates/frontend-review-checklist.md",
        "templates/permission-review-checklist.md",
        "templates/process-state-debugging.md",
    ]:
        assert (SKILL_ROOT / path).exists()
