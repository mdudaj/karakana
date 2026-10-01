from karakana.requirements.prd import generate_prd
from karakana.requirements.schemas import RequirementSource
from karakana.requirements.stories import generate_stories
from karakana.requirements.summary import render_prd, render_stories


CONCRETE_SOURCE = """## Specification / PRD Seed
Problem: Handoffs omit active project backlog items.
Goal: Let project maintainers find active backlog items from handoffs.
Users / Actors:
- project maintainer
Functional requirements:
- Handoffs link only their own project's active backlog.
- Completed-only backlogs are omitted from handoffs.
Acceptance criteria:
- A handoff for a project with open items links that project's backlog.
- A handoff for a completed-only backlog has no backlog link.
"""


def test_generic_source_produces_one_provisional_story():
    prd = generate_prd(RequirementSource(source_type="note"), "Add requirements storage, CLI, safety, evals, and tests.")

    stories = generate_stories(prd)

    assert len(stories) == 1
    assert stories[0].title.startswith("Needs review:")
    assert stories[0].actor.startswith("Needs review:")
    assert stories[0].want.startswith("Needs review:")
    assert stories[0].outcome.startswith("Needs review:")
    assert stories[0].acceptance_criteria[0].startswith("Needs review:")
    assert not prd.users_or_actors
    assert "Needs review: identify source users or actors." in render_prd(prd)
    assert "schema and storage" not in render_stories(stories)


def test_concrete_source_produces_requirement_drafts_with_unmapped_criteria():
    prd = generate_prd(RequirementSource(source_type="note"), CONCRETE_SOURCE)

    stories = generate_stories(prd)

    assert len(stories) == 2
    assert [story.want for story in stories] == prd.functional_requirements
    assert all(story.actor == "project maintainer" for story in stories)
    assert all(story.outcome == prd.goal for story in stories)
    assert all(story.acceptance_criteria == [f"Source criterion (mapping needs review): {item}" for item in prd.standards_spec.acceptance_criteria] for story in stories)
    assert "the capability described by this PRD" not in render_prd(prd)
    assert "Handoffs link only their own project's active backlog." in render_prd(prd)
    assert "Source criterion (mapping needs review)" in render_stories(stories)


def test_concrete_requirement_without_actor_or_goal_marks_only_missing_fields():
    source = """## Specification / PRD Seed
Functional requirements:
- Handoffs link the active project backlog.
Acceptance criteria:
- The handoff includes the correct project backlog link.
"""
    prd = generate_prd(RequirementSource(source_type="note"), source)

    story = generate_stories(prd)[0]

    assert story.want == "Handoffs link the active project backlog."
    assert story.acceptance_criteria == ["The handoff includes the correct project backlog link."]
    assert story.actor.startswith("Needs review:")
    assert story.outcome.startswith("Needs review:")
    assert "Actor: Needs review:" in render_stories([story])


def test_concrete_requirement_without_source_criteria_keeps_behavior_provisional():
    source = """## Specification / PRD Seed
Goal: Show project backlog links in handoffs.
Functional requirements:
- Handoffs link their own project's active backlog.
"""
    prd = generate_prd(RequirementSource(source_type="note"), source)

    story = generate_stories(prd)[0]

    assert story.want == "Handoffs link their own project's active backlog."
    assert story.acceptance_criteria == ["Needs review: add source-specific acceptance criteria."]


def test_msc_platform_story_generation_uses_research_slices():
    prd = generate_prd(RequirementSource(source_type="note"), "Milestone 22.6 cleanup", project="msc-platform")

    stories = generate_stories(prd)

    assert any(story.title == "Slice 1A: Curriculum source registry schema" for story in stories)
    assert any("Evidence artifact produced" in "\n".join(story.standards) for story in stories)


def test_msc_platform_story_generation_selects_curriculum_intake_ux_slice():
    prd = generate_prd(
        RequirementSource(source_type="note"),
        "Slice 1.1: Curriculum Intake Management UX and TIE Source Actions",
        project="msc-platform",
    )

    stories = generate_stories(prd)

    assert [story.title for story in stories] == [
        "Slice 1.1A: Staff curriculum intake management surface",
        "Slice 1.1B: Seed default TIE source action",
        "Slice 1.1C: Add or update TIE source action",
        "Slice 1.1D: Capture snapshot action",
    ]
    assert all("curriculum intake management" in story.want.lower() for story in stories)
