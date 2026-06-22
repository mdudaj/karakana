from pathlib import Path

from karakana.evals.loader import EvalLoader


def test_skill_promotion_policy_doc_exists():
    text = Path("docs/skill-promotion-policy.md").read_text(encoding="utf-8")

    assert "in-progress -> experimental -> stable -> deprecated" in text
    assert "Deprecation" in text


def test_skills_doc_describes_index_and_lifecycle_metadata():
    text = Path("docs/skills.md").read_text(encoding="utf-8")

    assert "Skill Indexes" in text
    assert "`status`" in text
    assert "`visibility`" in text
    assert "`bucket`" in text


def test_new_skill_evals_are_discoverable():
    ids = {case.id for case in EvalLoader(Path.cwd()).load_cases(suite="skills")}

    assert "skill-index-generation" in ids
    assert "handoff-includes-suggested-skills" in ids
    assert "new-skill-requires-eval" in ids
    assert "standards-vs-spec-review" in ids
