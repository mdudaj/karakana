from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.skills.index import generate_skill_index


def _write_index_skill(root: Path, name: str, metadata: str = "") -> None:
    skill_root = root / "skills" / name
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"""---
name: {name}
description: {name} description.
version: 0.1.0
risk_level: low
status: stable
visibility: public
bucket: development
allowed_tools:
  - read_file
requires_approval_for: []
{metadata}---
# {name}

## Purpose

Purpose.

## When to use this skill

Use it.

## When not to use this skill

Do not use it.

## Core concepts

- Concept.

## Standard workflow

1. Work.

## Safety rules

- Safe.

## Required checks

- Check.

## Output format

Return output.

## Examples

- Example.
""",
        encoding="utf-8",
    )


def test_hidden_skills_are_excluded_from_index(tmp_path: Path):
    _write_index_skill(tmp_path, "visible-skill")
    _write_index_skill(tmp_path, "hidden-skill", "visibility: hidden\n")

    index = generate_skill_index(tmp_path / "skills")

    assert "`visible-skill`" in index
    assert "hidden-skill" not in index


def test_deprecated_status_is_marked_in_index(tmp_path: Path):
    _write_index_skill(tmp_path, "old-skill", "status: deprecated\n")

    index = generate_skill_index(tmp_path / "skills")

    assert "`old-skill`" in index
    assert "**deprecated**" in index


def test_skill_index_cli_dry_run_does_not_write(tmp_path: Path, monkeypatch):
    _write_index_skill(tmp_path, "visible-skill")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["skill", "index"])

    assert result.exit_code == 0
    assert "Dry run: no files written" in result.output
    assert "`visible-skill`" in result.output
    assert not (tmp_path / "skills" / "README.md").exists()


def test_skill_index_cli_write_updates_readme(tmp_path: Path, monkeypatch):
    _write_index_skill(tmp_path, "visible-skill")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["skill", "index", "--write"])

    assert result.exit_code == 0
    readme = tmp_path / "skills" / "README.md"
    assert readme.exists()
    assert "`visible-skill`" in readme.read_text(encoding="utf-8")
