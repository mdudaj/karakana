"""Render configuration summaries."""

from __future__ import annotations

import json
from pathlib import Path

from karakana.config.schemas import KarakanaConfig


def render_config(config: KarakanaConfig) -> str:
    return json.dumps(config.to_dict(), indent=2, sort_keys=True) + "\n"


def render_config_validation(errors: list[str], warnings: list[str]) -> str:
    status = "passed" if not errors else "failed"
    lines = [f"Config validation: {status}", "", "Errors:"]
    lines.extend([f"- {error}" for error in errors] or ["- None"])
    lines.append("")
    lines.append("Warnings:")
    lines.extend([f"- {warning}" for warning in warnings] or ["- None"])
    return "\n".join(lines) + "\n"


def render_paths(repo_root: Path, config: KarakanaConfig) -> str:
    artifact_root = repo_root / config.paths.artifacts
    lines = [
        "Karakana paths",
        f"- repo root: {repo_root}",
        f"- artifact root: {artifact_root}",
        f"- ubongo root: {repo_root / config.paths.ubongo}",
        f"- skills root: {repo_root / config.paths.skills}",
        f"- skillpacks root: {repo_root / config.paths.skillpacks}",
        f"- workspaces root: {repo_root / config.paths.workspaces}",
        f"- current workspace state: {artifact_root / 'current-workspace.json'}",
        f"- current skillpack state: {artifact_root / 'current-skillpack.json'}",
    ]
    return "\n".join(lines) + "\n"
