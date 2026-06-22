"""Lightweight repository context collection."""

from __future__ import annotations

import subprocess
from pathlib import Path


def collect_repository_context(repo_root: Path) -> str:
    """Collect safe, local repository context for generated prompts."""
    lines: list[str] = []
    lines.append(f"Repository root: {repo_root}")
    lines.append(f"Git branch: {_git_branch(repo_root)}")
    lines.append("")
    lines.append("Top-level paths:")
    for path in _top_level_paths(repo_root):
        suffix = "/" if path.is_dir() else ""
        lines.append(f"- {path.name}{suffix}")

    status = _git_status(repo_root)
    if status:
        lines.append("")
        lines.append("Git status --short:")
        lines.extend(f"- {line}" for line in status.splitlines())
    return "\n".join(lines).strip() + "\n"


def _top_level_paths(repo_root: Path) -> list[Path]:
    ignored = {".git", ".venv", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".karakana"}
    if not repo_root.exists():
        return []
    return sorted((path for path in repo_root.iterdir() if path.name not in ignored), key=lambda path: path.name)


def _git_branch(repo_root: Path) -> str:
    return _run_git(repo_root, ["git", "branch", "--show-current"]) or "unknown"


def _git_status(repo_root: Path) -> str:
    return _run_git(repo_root, ["git", "status", "--short"])


def _run_git(repo_root: Path, command: list[str]) -> str:
    try:
        result = subprocess.run(command, cwd=repo_root, check=False, capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()
