"""Patch apply operations with dry-run defaults."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from karakana.codex.schemas import PatchArtifact
from karakana.patch.gates import run_patch_gate
from karakana.patch.schemas import PatchApplyResult
from karakana.safety.patch import validate_patch_apply
from karakana.tools.code_search import _git_branch


def apply_patch_run(repo_root: Path, patch_run_id: str, write: bool = False, stage: bool = False, allow_high_risk: bool = False, allow_main: bool = False) -> PatchApplyResult:
    artifact = _load_patch(repo_root, patch_run_id)
    diff_path = Path(artifact.diff_path or "")
    gate, _ = run_patch_gate(repo_root, patch_run_id)
    current_branch = _git_branch(repo_root)
    failures = validate_patch_apply(gate.blocked, gate.risk_level, current_branch, write, allow_high_risk=allow_high_risk, allow_main=allow_main)
    if failures:
        return PatchApplyResult(patch_run_id, "blocked", dry_run=not write, applied=False, files_changed=artifact.files_changed, warnings=gate.warnings, errors=failures)
    check = _git(repo_root, ["apply", "--check", str(diff_path)])
    if check.returncode != 0:
        return PatchApplyResult(patch_run_id, "conflict", dry_run=True, applied=False, files_changed=artifact.files_changed, conflicts=[check.stderr.strip()], warnings=gate.warnings)
    if not write:
        return PatchApplyResult(patch_run_id, "dry_run_passed", dry_run=True, applied=False, files_changed=artifact.files_changed, warnings=gate.warnings)
    applied = _git(repo_root, ["apply", str(diff_path)])
    if applied.returncode != 0:
        return PatchApplyResult(patch_run_id, "error", dry_run=False, applied=False, files_changed=artifact.files_changed, errors=[applied.stderr.strip()])
    if stage and artifact.files_changed:
        _git(repo_root, ["add", *artifact.files_changed])
    return PatchApplyResult(patch_run_id, "applied", dry_run=False, applied=True, files_changed=artifact.files_changed, warnings=gate.warnings)


def _load_patch(repo_root: Path, patch_run_id: str) -> PatchArtifact:
    path = repo_root / ".karakana" / "patches" / patch_run_id / "patch.json"
    if not path.exists():
        raise FileNotFoundError(f"Patch artifact not found: {patch_run_id}")
    return PatchArtifact.from_dict(json.loads(path.read_text(encoding="utf-8")))


def _git(repo_root: Path, command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *command], cwd=repo_root, capture_output=True, text=True, check=False)
