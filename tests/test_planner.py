from pathlib import Path

import pytest

from karakana.agents.planner import compose_planning_prompt, write_planning_prompt
from karakana.memory.ubongo import REQUIRED_GLOBAL_FILES, REQUIRED_PROJECT_FILES


def write_memory_tree(root: Path, project: str = "karakana") -> None:
    global_root = root / "ubongo" / "global"
    project_root = root / "ubongo" / "projects" / project
    global_root.mkdir(parents=True, exist_ok=True)
    project_root.mkdir(parents=True, exist_ok=True)
    for filename in REQUIRED_GLOBAL_FILES:
        (global_root / filename).write_text(f"# {filename}\n\nGlobal planning context.\n", encoding="utf-8")
    for filename in REQUIRED_PROJECT_FILES:
        (project_root / filename).write_text(f"# {filename}\n\nProject planning context.\n", encoding="utf-8")


def write_skill(root: Path, name: str = "example-skill") -> None:
    skill_root = root / "skills" / name
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"""---
name: {name}
description: Use this skill for planning tests.
version: 0.1.0
risk_level: low
allowed_tools:
  - read_file
requires_approval_for: []
---
# Example Skill

## Purpose

Support deterministic planning tests.

## When to use this skill

Use in tests.

## When not to use this skill

Do not use outside tests.

## Core concepts

- Deterministic prompt composition.

## Standard workflow

1. Compose.

## Safety rules

- No external calls.

## Required checks

- Run tests.

## Output format

Return prompt.

## Examples

- Compose a plan.
""",
        encoding="utf-8",
    )


def test_compose_planning_prompt_includes_context(tmp_path):
    write_memory_tree(tmp_path)
    write_skill(tmp_path)
    (tmp_path / "KARAKANA.md").write_text("# Contract\n\nProject contract content.\n", encoding="utf-8")

    prompt = compose_planning_prompt(
        project="karakana",
        skill="example-skill",
        task="Design the next improvement loop",
        repo_root=tmp_path,
    )

    assert "# Karakana Planning Task" in prompt
    assert "Design the next improvement loop" in prompt
    assert "Name: example-skill" in prompt
    assert "Project planning context" in prompt
    assert "Project contract content" in prompt
    assert "Do not call external model APIs" in prompt


def test_compose_planning_prompt_errors_for_missing_project_memory(tmp_path):
    write_skill(tmp_path)

    with pytest.raises(FileNotFoundError, match="missing required memory files"):
        compose_planning_prompt("karakana", "example-skill", "Task", tmp_path)


def test_compose_planning_prompt_errors_for_missing_skill(tmp_path):
    write_memory_tree(tmp_path)

    with pytest.raises(FileNotFoundError, match="Skill not found"):
        compose_planning_prompt("karakana", "missing-skill", "Task", tmp_path)


def test_write_planning_prompt_creates_runtime_file(tmp_path):
    path = write_planning_prompt("prompt", repo_root=tmp_path)

    assert path == tmp_path / ".karakana" / "planning-task.md"
    assert path.read_text(encoding="utf-8") == "prompt"
