"""Draft release notes from local evidence."""

from __future__ import annotations

import json
import secrets
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from karakana.release.metadata import package_version


def generate_release_notes(repo_root: Path, version: str | None = None, since: str | None = None) -> tuple[str, Path]:
    notes_id = _release_id("notes")
    directory = repo_root / ".karakana" / "release" / notes_id
    directory.mkdir(parents=True, exist_ok=True)
    log_lines = _git_log(repo_root, since)
    eval_count = len(list((repo_root / ".karakana" / "eval-runs").glob("*"))) if (repo_root / ".karakana" / "eval-runs").exists() else 0
    crosslink_count = len(list((repo_root / ".karakana" / "crosslinks").glob("*"))) if (repo_root / ".karakana" / "crosslinks").exists() else 0
    selected_version = version or package_version()
    markdown = f"""# Karakana Release Notes

## Version

{selected_version}

## Summary

Draft release notes generated from local repository evidence only. Review before publishing.

## Added

- Local harness features and artifacts captured in the current working tree.

## Changed

- See recent git log entries below.

## Fixed

- Needs review.

## Safety

- No publishing, tags, pushes, releases, deployments, live model calls, or remote writes were performed.

## Documentation

- Review README, AGENTS, and docs before release.

## Tests and Evals

- Recent eval run artifacts found: {eval_count}
- Recent crosslink artifacts found: {crosslink_count}

## Known Limitations

- Release notes are draft-only and deterministic.

## Upgrade Notes

- Needs review.

## Release Checklist

- Run `karakana release checklist`.

## Recent Git Log

{_format_log(log_lines)}
"""
    md_path = directory / "release-notes.md"
    json_path = directory / "release-notes.json"
    md_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps({"release_notes_id": notes_id, "version": selected_version, "since": since, "path": str(md_path)}, indent=2) + "\n", encoding="utf-8")
    return notes_id, md_path


def _git_log(repo_root: Path, since: str | None) -> list[str]:
    args = ["git", "log", "--oneline", "-n", "20"]
    if since:
        args = ["git", "log", "--oneline", f"{since}..HEAD"]
    try:
        result = subprocess.run(args, cwd=repo_root, text=True, capture_output=True, check=False)
    except FileNotFoundError:
        return ["git not available"]
    return [line for line in result.stdout.splitlines() if line.strip()] or ["No git log entries available."]


def _format_log(lines: list[str]) -> str:
    return "\n".join(f"- {line}" for line in lines)


def _release_id(kind: str) -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-release-{kind}-{secrets.token_hex(3)}"
