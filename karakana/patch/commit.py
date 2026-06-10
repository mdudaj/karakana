"""Local commit operations for applied patches."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from karakana.codex.schemas import PatchArtifact
from karakana.patch.gates import run_patch_gate
from karakana.patch.schemas import PatchCommitResult
from karakana.safety.patch import validate_patch_commit
from karakana.tools.code_search import _git_branch


def commit_patch_run(repo_root: Path, patch_run_id: str, message: str, write: bool = False, stage: bool = False, allow_high_risk: bool = False, allow_main: bool = False) -> PatchCommitResult:
    artifact = _load_patch(repo_root, patch_run_id)
    gate, _ = run_patch_gate(repo_root, patch_run_id)
    current_branch = _git_branch(repo_root)
    if stage and artifact.files_changed:
        _git(repo_root, ["add", *artifact.files_changed])
    staged = bool(_git(repo_root, ["diff", "--cached", "--name-only"]).stdout.strip())
    if not message or not message.strip():
        return PatchCommitResult(patch_run_id, "blocked", committed=False, message=message, warnings=gate.warnings, errors=["commit message is required"])
    if not write:
        warnings = ["Dry run only. Pass --write to create a local commit."]
        if gate.blocked:
            warnings.append("Patch gate is blocked; commit would be refused in write mode.")
        if gate.risk_level in {"high", "critical"}:
            warnings.append("High-risk patch requires --allow-high-risk in write mode.")
        if not staged:
            warnings.append("No staged changes are currently available to commit.")
        return PatchCommitResult(patch_run_id, "dry_run", committed=False, message=message, warnings=warnings)
    failures = validate_patch_commit(gate.blocked, gate.risk_level, current_branch, message, staged, allow_high_risk=allow_high_risk, allow_main=allow_main)
    if failures:
        return PatchCommitResult(patch_run_id, "blocked", committed=False, message=message, warnings=gate.warnings, errors=failures)
    result = _git(repo_root, ["commit", "-m", message])
    if result.returncode != 0:
        return PatchCommitResult(patch_run_id, "error", committed=False, message=message, errors=[result.stderr.strip()])
    sha = _git(repo_root, ["rev-parse", "HEAD"]).stdout.strip()
    return PatchCommitResult(patch_run_id, "committed", committed=True, commit_sha=sha, message=message)


def _load_patch(repo_root: Path, patch_run_id: str) -> PatchArtifact:
    path = repo_root / ".karakana" / "patches" / patch_run_id / "patch.json"
    if not path.exists():
        raise FileNotFoundError(f"Patch artifact not found: {patch_run_id}")
    return PatchArtifact.from_dict(json.loads(path.read_text(encoding="utf-8")))


def _git(repo_root: Path, command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *command], cwd=repo_root, capture_output=True, text=True, check=False)
