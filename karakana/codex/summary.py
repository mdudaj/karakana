"""Patch summary helpers."""

from __future__ import annotations

import json
from pathlib import Path

from karakana.codex.schemas import PatchArtifact
from karakana.codex.reviewer import changed_files_from_diff


def summarize_patch(repo_root: Path, patch_run_id: str) -> Path:
    patch_root = repo_root / ".karakana" / "patches" / patch_run_id
    patch_json = patch_root / "patch.json"
    if patch_json.exists():
        artifact = PatchArtifact.from_dict(json.loads(patch_json.read_text(encoding="utf-8")))
    else:
        diff_path = patch_root / "changes.diff"
        files = changed_files_from_diff(diff_path.read_text(encoding="utf-8") if diff_path.exists() else "")
        artifact = PatchArtifact(patch_run_id, None, "", None, None, str(diff_path), str(patch_root / "summary.md"), None, files)
    summary = patch_root / "summary.md"
    summary.write_text(_render_summary(artifact), encoding="utf-8")
    return summary


def _render_summary(artifact: PatchArtifact) -> str:
    return f"""# Karakana Patch Summary

## Summary

- Patch run ID: {artifact.patch_run_id}
- Source task ID: {artifact.source_task_id or ""}
- Git branch: {artifact.git_branch or ""}
- Files changed: {len(artifact.files_changed)}

## Likely Intent

Review the changed files and associated patch review to infer implementation intent.

## Files Changed

{_bullets(artifact.files_changed)}

## Risk Signals

{_risk_signals(artifact.files_changed)}

## Patch Review

Run `karakana codex review-patch --diff {artifact.diff_path}` for deterministic review.
"""


def _risk_signals(files: list[str]) -> str:
    signals = []
    for path in files:
        lowered = path.lower()
        if ".github/workflows" in lowered:
            signals.append("GitHub workflow change")
        if "migration" in lowered:
            signals.append("Migration change")
        if "billing" in lowered or "payment" in lowered:
            signals.append("Payment or billing change")
    return _bullets(sorted(set(signals)))


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)
