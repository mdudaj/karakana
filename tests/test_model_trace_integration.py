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
        (global_root / filename).write_text(f"# {filename}\n\nGlobal model context.\n", encoding="utf-8")
    for filename in REQUIRED_PROJECT_FILES:
        (project_root / filename).write_text(f"# {filename}\n\nProject model context.\n", encoding="utf-8")


def write_skill(root: Path, name: str = "karakana-self-improvement") -> None:
    skill_root = root / "skills" / name
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"""---
name: {name}
description: Use this skill for model integration tests.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
requires_approval_for: []
---
# Karakana Self Improvement

## Purpose

Model tests.

## When to use this skill

Use in tests.

## When not to use this skill

Do not use outside tests.

## Core concepts

- Model artifacts only.

## Standard workflow

1. Generate prompt.

## Safety rules

- No mutation.

## Required checks

- Run tests.

## Output format

Return response.

## Examples

- Run mock model.
""",
        encoding="utf-8",
    )


def test_plan_dry_run_by_default(tmp_path, monkeypatch):
    write_memory_tree(tmp_path)
    write_skill(tmp_path)
    (tmp_path / "KARAKANA.md").write_text("# Contract\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        ["plan", "--project", "karakana", "--skill", "karakana-self-improvement", "--task", "Design provider abstraction follow-up"],
    )

    latest = TraceStore(tmp_path).latest()
    assert result.exit_code == 0
    assert latest.outputs.get("model_response_path") is None


def test_plan_live_mock_writes_model_response(tmp_path, monkeypatch):
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
            "Design provider abstraction follow-up",
            "--provider",
            "mock",
            "--model",
            "mock-model",
            "--live",
        ],
    )

    latest = TraceStore(tmp_path).latest()
    assert result.exit_code == 0
    assert latest.outputs["provider"] == "mock"
    assert latest.outputs["model"] == "mock-model"
    response_path = Path(latest.outputs["model_response_artifact"])
    assert response_path.exists()
    assert "[MOCK MODEL RESPONSE]" in response_path.read_text(encoding="utf-8")
    assert Path(latest.outputs["response_review_artifact"]).exists()
