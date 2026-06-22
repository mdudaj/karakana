from pathlib import Path

import pytest

from karakana.memory.ubongo import REQUIRED_GLOBAL_FILES, REQUIRED_PROJECT_FILES
from karakana.tools.codex_executor import CodexExecutor


def write_memory_tree(root: Path, project: str = "karakana") -> None:
    global_root = root / "ubongo" / "global"
    project_root = root / "ubongo" / "projects" / project
    global_root.mkdir(parents=True, exist_ok=True)
    project_root.mkdir(parents=True, exist_ok=True)
    for filename in REQUIRED_GLOBAL_FILES:
        (global_root / filename).write_text(f"# {filename}\n\nGlobal Codex context.\n", encoding="utf-8")
    for filename in REQUIRED_PROJECT_FILES:
        (project_root / filename).write_text(f"# {filename}\n\nProject Codex context.\n", encoding="utf-8")


def write_skill(root: Path, name: str = "karakana-self-improvement") -> None:
    skill_root = root / "skills" / name
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"""---
name: {name}
description: Use this skill for Codex task tests.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
requires_approval_for:
  - skill_update
---
# Karakana Self Improvement

## Purpose

Support Codex task tests.

## When to use this skill

Use in tests.

## When not to use this skill

Do not use outside tests.

## Core concepts

- Reviewable task generation.

## Standard workflow

1. Generate prompt.

## Safety rules

- No automatic execution.

## Required checks

- Run tests.

## Output format

Return prompt.

## Examples

- Generate a Codex task.
""",
        encoding="utf-8",
    )


def test_build_task_prompt_includes_required_context(tmp_path):
    write_memory_tree(tmp_path)
    write_skill(tmp_path)
    (tmp_path / "KARAKANA.md").write_text("# Contract\n\nProject contract content.\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# Agents\n\nRepository instructions.\n", encoding="utf-8")

    prompt = CodexExecutor(tmp_path).build_task_prompt(
        project="karakana",
        skill="karakana-self-improvement",
        task="Implement reflection trace schema",
        focus="schema, tests, and safety",
    )

    assert "# Karakana Codex Task" in prompt
    assert "Implement reflection trace schema" in prompt
    assert "Focus: schema, tests, and safety" in prompt
    assert "Project Codex context" in prompt
    assert "Name: karakana-self-improvement" in prompt
    assert "Project contract content" in prompt
    assert "Repository instructions." in prompt
    assert "Do not push directly to main" in prompt
    assert "skill_update" in prompt


def test_write_task_prompt_defaults_to_runtime_file(tmp_path):
    path = CodexExecutor(tmp_path).write_task_prompt("prompt")

    assert path == tmp_path / ".karakana" / "codex-task.md"
    assert path.read_text(encoding="utf-8") == "prompt"


def test_build_task_prompt_errors_for_missing_project(tmp_path):
    write_skill(tmp_path)

    with pytest.raises(FileNotFoundError, match="missing required memory files"):
        CodexExecutor(tmp_path).build_task_prompt("karakana", "karakana-self-improvement", "Task")


def test_build_task_prompt_errors_for_missing_skill(tmp_path):
    write_memory_tree(tmp_path)

    with pytest.raises(FileNotFoundError, match="Skill not found"):
        CodexExecutor(tmp_path).build_task_prompt("karakana", "missing", "Task")
