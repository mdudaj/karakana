from karakana.requirements.prd import generate_prd
from karakana.requirements.schemas import RequirementSource
from karakana.requirements.stories import generate_stories


def test_story_generation_vertical_slices():
    prd = generate_prd(RequirementSource(source_type="note"), "Add requirements storage, CLI, safety, evals, and tests.")

    stories = generate_stories(prd)

    assert len(stories) >= 5
    assert all(story.acceptance_criteria for story in stories)
    assert any("schema and storage" in story.title for story in stories)
