"""Patch lifecycle summary command helpers."""

from __future__ import annotations

from pathlib import Path

from karakana.patch.status import write_patch_status


def summarize_patch_lifecycle(repo_root: Path, patch_run_id: str) -> Path:
    path, _ = write_patch_status(repo_root, patch_run_id)
    return path
