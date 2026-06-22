from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.memory.ubongo import REQUIRED_GLOBAL_FILES, REQUIRED_PROJECT_FILES


def write_memory_tree(root: Path, project: str = "karakana") -> None:
    global_root = root / "ubongo" / "global"
    project_root = root / "ubongo" / "projects" / project
    global_root.mkdir(parents=True, exist_ok=True)
    project_root.mkdir(parents=True, exist_ok=True)
    for filename in REQUIRED_GLOBAL_FILES:
        (global_root / filename).write_text(f"# {filename}\n\nGlobal CLI planning context.\n", encoding="utf-8")
    for filename in REQUIRED_PROJECT_FILES:
        (project_root / filename).write_text(f"# {filename}\n\nProject CLI planning context.\n", encoding="utf-8")


def write_skill(root: Path, name: str = "karakana-self-improvement") -> None:
    skill_root = root / "skills" / name
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"""---
name: {name}
description: Use this skill for CLI planning tests.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
requires_approval_for:
  - skill_update
---
# Karakana Self Improvement

## Purpose

Support CLI planning tests.

## When to use this skill

Use in tests.

## When not to use this skill

Do not use outside tests.

## Core concepts

- Reviewable improvement.

## Standard workflow

1. Plan.

## Safety rules

- No external calls.

## Required checks

- Run tests.

## Output format

Return plan.

## Examples

- Design an improvement loop.
""",
        encoding="utf-8",
    )


def test_plan_cli_writes_prompt(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    write_skill(tmp_path)
    (tmp_path / "KARAKANA.md").write_text("# Contract\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        [
            "plan",
            "--project",
            "karakana",
            "--skill",
            "karakana-self-improvement",
            "--task",
            "Design the next improvement loop",
        ],
    )

    output = tmp_path / ".karakana" / "planning-task.md"
    assert result.exit_code == 0
    assert "Selected model: gpt-5-mini" in result.output
    assert f"Prompt written to: {output}" in result.output
    assert output.exists()
    assert "Design the next improvement loop" in output.read_text(encoding="utf-8")


def test_plan_cli_reports_missing_skill(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        ["plan", "--project", "karakana", "--skill", "missing", "--task", "Task"],
    )

    assert result.exit_code == 1
    assert "Skill not found" in result.output
