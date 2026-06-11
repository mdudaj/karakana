"""Documentation command helpers."""

from __future__ import annotations

from pathlib import Path

from karakana.docs.command_reference import render_command_reference

REQUIRED_DOCS = [
    "README.md",
    "AGENTS.md",
    "KARAKANA.md",
    "docs/skills.md",
    "docs/skillpacks.md",
    "docs/workspaces.md",
    "docs/skill-vs-tool-policy.md",
    "docs/skill-promotion-policy.md",
    "docs/command-reference.md",
]


def command_reference(repo_root: Path, write: bool = False) -> tuple[str, Path]:
    text = render_command_reference()
    path = repo_root / "docs" / "command-reference.md"
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return text, path


def check_docs(repo_root: Path) -> tuple[list[str], list[str]]:
    missing = [path for path in REQUIRED_DOCS if not (repo_root / path).exists()]
    warnings: list[str] = []
    if missing:
        warnings.extend(f"Missing required doc: {path}" for path in missing)
    return missing, warnings
