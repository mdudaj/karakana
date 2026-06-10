from pathlib import Path

from karakana.skillpacks.loader import SkillpackLoader


def test_skillpack_loader_discovery():
    loader = SkillpackLoader(Path.cwd())

    names = loader.list_skillpacks()

    assert "karakana" in names
    assert "nhrdm" in names


def test_load_one_skillpack():
    skillpack = SkillpackLoader(Path.cwd()).load("billing")

    assert skillpack.project.id == "billing"
    assert "gepg-billing" in skillpack.skills.required
