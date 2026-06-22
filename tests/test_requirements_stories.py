from karakana.requirements.prd import generate_prd
from karakana.requirements.schemas import RequirementSource
from karakana.requirements.stories import generate_stories


def test_story_generation_vertical_slices():
    prd = generate_prd(RequirementSource(source_type="note"), "Add requirements storage, CLI, safety, evals, and tests.")

    stories = generate_stories(prd)

    assert len(stories) >= 5
    assert all(story.acceptance_criteria for story in stories)
    assert any("schema and storage" in story.title for story in stories)


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
