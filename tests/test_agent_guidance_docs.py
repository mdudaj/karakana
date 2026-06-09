from pathlib import Path


def test_skill_vs_tool_policy_exists_and_has_required_guidance():
    text = Path("docs/skill-vs-tool-policy.md").read_text(encoding="utf-8")

    assert "Prefer a Skill When" in text
    assert "Create a Tool When" in text
    assert "Skills describe workflows" in text
    assert "Posting GitHub comments -> tool" in text


def test_agents_md_contains_expected_guidance_sections():
    text = Path("AGENTS.md").read_text(encoding="utf-8")

    for section in [
        "## Repository Entry Points",
        "## Standard Commands",
        "## How to Add a Skill",
        "## How to Add a Tool",
        "## How to Update Ubongo",
        "## How to Run Evals",
        "## Safety Rules",
        "## Files Requiring Extra Caution",
        "## Pull Request Expectations",
    ]:
        assert section in text


def test_skills_doc_explains_optional_activation_metadata():
    text = Path("docs/skills.md").read_text(encoding="utf-8")

    assert "activation" in text
    assert "scope" in text
    assert "category" in text
    assert "karakana eval run --skill" in text
