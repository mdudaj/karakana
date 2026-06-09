from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.memory.ubongo import REQUIRED_GLOBAL_FILES, REQUIRED_PROJECT_FILES
from karakana.traces.store import TraceStore


def write_memory_tree(root: Path, project: str = "karakana") -> None:
    global_root = root / "ubongo" / "global"
    project_root = root / "ubongo" / "projects" / project
    global_root.mkdir(parents=True, exist_ok=True)
    project_root.mkdir(parents=True, exist_ok=True)
    for filename in REQUIRED_GLOBAL_FILES:
        (global_root / filename).write_text(f"# {filename}\n\nGlobal trace context.\n", encoding="utf-8")
    for filename in REQUIRED_PROJECT_FILES:
        (project_root / filename).write_text(f"# {filename}\n\nProject trace context.\n", encoding="utf-8")


def write_skill(root: Path, name: str = "karakana-self-improvement") -> None:
    skill_root = root / "skills" / name
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"""---
name: {name}
description: Use this skill for trace integration tests.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
requires_approval_for:
  - skill_update
---
# Karakana Self Improvement

## Purpose

Trace integration.

## When to use this skill

Use in tests.

## When not to use this skill

Do not use outside tests.

## Core concepts

- Trace evidence.

## Standard workflow

1. Run command.

## Safety rules

- Local only.

## Required checks

- Run tests.

## Output format

Return trace.

## Examples

- Trace a command.
""",
        encoding="utf-8",
    )


def test_plan_success_creates_trace(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    write_skill(tmp_path)
    (tmp_path / "KARAKANA.md").write_text("# Contract\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        ["plan", "--project", "karakana", "--skill", "karakana-self-improvement", "--task", "Design a reflection loop"],
    )

    latest = TraceStore(tmp_path).latest()
    assert result.exit_code == 0
    assert latest is not None
    assert latest.command == "plan"
    assert latest.status == "success"
    assert latest.artifacts[0].kind == "planning_prompt"
    assert (tmp_path / ".karakana" / "runs" / latest.run_id / "trace.json").exists()
    assert (tmp_path / ".karakana" / "runs" / latest.run_id / "summary.md").exists()


def test_plan_failure_creates_failed_trace(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        ["plan", "--project", "karakana", "--skill", "missing", "--task", "Design a reflection loop"],
    )

    latest = TraceStore(tmp_path).latest()
    assert result.exit_code == 1
    assert latest is not None
    assert latest.command == "plan"
    assert latest.status == "failed"
    assert latest.errors


def test_memory_validate_failure_creates_failed_trace(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    (tmp_path / "ubongo" / "projects" / "karakana" / "open-issues.md").unlink()
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["memory", "validate", "--project", "karakana"])

    latest = TraceStore(tmp_path).latest()
    assert result.exit_code == 1
    assert latest is not None
    assert latest.command == "memory validate"
    assert latest.status == "failed"
    assert "open-issues.md" in latest.outputs["missing_files"]
