"""Local branch planning and creation for reviewed patches."""

from __future__ import annotations

import subprocess
from pathlib import Path

from karakana.patch.schemas import PatchBranchPlan
from karakana.safety.patch import validate_branch_creation
from karakana.tools.code_search import _git_branch


def plan_patch_branch(repo_root: Path, patch_run_id: str, base: str = "main", name: str | None = None) -> PatchBranchPlan:
    current = _git_branch(repo_root)
    proposed = name or f"karakana/patch-{patch_run_id}"
    exists = _branch_exists(repo_root, proposed)
    dirty = bool(_git(repo_root, ["status", "--short"]).strip())
    warnings = validate_branch_creation(proposed, current, dirty, exists=exists)
    return PatchBranchPlan(patch_run_id, current, proposed, base, can_create=not warnings, warnings=warnings)


def create_patch_branch(repo_root: Path, patch_run_id: str, base: str = "main", name: str | None = None, allow_dirty: bool = False, reuse: bool = False) -> PatchBranchPlan:
    current = _git_branch(repo_root)
    proposed = name or f"karakana/patch-{patch_run_id}"
    exists = _branch_exists(repo_root, proposed)
    dirty = bool(_git(repo_root, ["status", "--short"]).strip())
    warnings = validate_branch_creation(proposed, current, dirty, allow_dirty=allow_dirty, reuse=reuse, exists=exists)
    if warnings:
        return PatchBranchPlan(patch_run_id, current, proposed, base, can_create=False, warnings=warnings)
    if exists and reuse:
        _git(repo_root, ["switch", proposed])
    else:
        _git(repo_root, ["switch", "-c", proposed])
    return PatchBranchPlan(patch_run_id, current, proposed, base, can_create=True, warnings=[])


def _branch_exists(repo_root: Path, name: str) -> bool:
    result = subprocess.run(["git", "rev-parse", "--verify", name], cwd=repo_root, capture_output=True, text=True, check=False)
    return result.returncode == 0


def _git(repo_root: Path, command: list[str]) -> str:
    result = subprocess.run(["git", *command], cwd=repo_root, capture_output=True, text=True, check=False)
    return result.stdout
