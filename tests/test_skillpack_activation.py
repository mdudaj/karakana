from pathlib import Path

from karakana.skillpacks.activation import SkillpackActivation


def test_skillpack_activation_writes_current():
    root = Path.cwd()
    state = SkillpackActivation(root).activate("karakana")
    current = SkillpackActivation(root).current()

    assert state["skillpack"] == "karakana"
    assert current["project"] == "karakana"
