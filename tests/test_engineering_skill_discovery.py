"""Catalogue/profile integration: optional choices, explicit selection and isolation."""

from pathlib import Path
import re

import pytest
from typer.testing import CliRunner

from karakana.cli import app
from karakana.memory.ubongo import REQUIRED_PROJECT_FILES
from karakana.skillpacks.loader import SkillpackLoader
from karakana.skillpacks.resolver import SkillpackResolver
from karakana.skills.index import generate_skill_index
from karakana.skills.loader import SkillLoader


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "engineering-requirements", "engineering-design-records",
    "engineering-delivery-planning", "engineering-release-documentation",
    "engineering-workbooks",
)
PROJECTS = ("karakana", "lims", "ent-meal")


def prepare_memory(root):
    """Controlled project markers make unintended context mixing observable."""
    for project in PROJECTS:
        folder = root / "ubongo" / "projects" / project
        folder.mkdir(parents=True, exist_ok=True)
        for filename in REQUIRED_PROJECT_FILES:
            (folder / filename).write_text(f"# Synthetic {filename}\n\nMEMORY_ONLY_{project}\n")


def selected_segment(prompt):
    return prompt.split("## Selected Skill\n", 1)[1].split("## Project Memory\n", 1)[0]


def test_committed_catalogue_is_current_and_experimental():
    assert (ROOT / "skills/README.md").read_text() == generate_skill_index(ROOT / "skills")
    loader = SkillLoader(ROOT / "skills")
    for name in SKILLS:
        skill = loader.load_skill(name)
        assert skill.status == "experimental" and skill.visibility == "public"
        assert f"| `{name}` | **experimental** |" in (ROOT / "skills/README.md").read_text()


def test_optional_enablement_is_limited_to_target_profiles():
    loader = SkillpackLoader(ROOT)
    for name in loader.list_skillpacks():
        context = SkillpackResolver(ROOT).resolve_for_project(name)
        assert not set(SKILLS) & set(context.required_skills)
        if name in PROJECTS:
            assert set(SKILLS) <= set(context.optional_skills)
            assert context.memory_path == f"ubongo/projects/{name}"
        else:
            assert not set(SKILLS) & set(context.optional_skills)


@pytest.mark.parametrize("project", PROJECTS)
@pytest.mark.parametrize("skill", SKILLS)
def test_explicit_documentation_choice_loads_one_body_and_project(project, skill, isolated_repo):
    prepare_memory(isolated_repo)
    output = Path(".karakana/chosen.md")
    result = CliRunner().invoke(app, ["plan", "--project", project, "--use-skillpack",
        "--skill", skill, "--task", "Plan the requested documentation review; do not draft release artifacts.",
        "--no-handoff", "--output", str(output)])
    assert result.exit_code == 0, result.output
    prompt = (isolated_repo / output).read_text()
    selected = selected_segment(prompt)
    assert f"Name: {skill}\n" in selected
    assert f"\n# {skill}\n" in selected
    assert all(f"\n# {other}\n" not in selected for other in SKILLS if other != skill)
    assert f"MEMORY_ONLY_{project}" in prompt
    assert all(f"MEMORY_ONLY_{other}" not in prompt for other in PROJECTS if other != project)
    assert "Catalogue availability does not authorize drafting" in prompt
    assert "## Optional Skills" in prompt
    assert "Do not call external model APIs" in prompt


@pytest.mark.parametrize("project", PROJECTS)
def test_unrelated_task_keeps_existing_default_skill(project, isolated_repo):
    prepare_memory(isolated_repo)
    context = SkillpackResolver(isolated_repo).resolve_for_project(project)
    result = CliRunner().invoke(app, ["plan", "--project", project, "--use-skillpack",
        "--task", "Review a bounded existing implementation bug", "--no-handoff"])
    assert result.exit_code == 0, result.output
    prompt = (isolated_repo / ".karakana/planning-task.md").read_text()
    selected = selected_segment(prompt)
    assert f"Name: {context.required_skills[0]}\n" in selected
    assert all(f"\n# {skill}\n" not in selected for skill in SKILLS)


def test_documentation_discovery_links_resolve_from_harness():
    for relative in ("ubongo/global/engineering-standards.md", "docs/engineering-process.md"):
        source = ROOT / relative
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", source.read_text()):
            if "://" in link or link.startswith("#"):
                continue
            path = (source.parent / link.split("#", 1)[0]).resolve()
            assert path.is_relative_to(ROOT) and path.is_file(), (relative, link)
