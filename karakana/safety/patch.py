"""Safety helpers for patch lifecycle operations."""

from __future__ import annotations

from pathlib import Path

from karakana.codex.reviewer import BLOCKING_PATTERNS, HIGH_RISK_PATTERNS, changed_files_from_diff

MAIN_BRANCHES = {"main", "master"}


def detect_patch_blocking_signals(diff: str, files_changed: list[str] | None = None) -> list[str]:
    lowered = "\n".join(_added_lines(diff)).lower()
    files = files_changed or changed_files_from_diff(diff)
    signals: list[str] = []
    if any(Path(path).name == ".env" or Path(path).name.startswith(".env.") for path in files):
        signals.append("env_exposure")
    for finding_type, patterns in BLOCKING_PATTERNS.items():
        for pattern in patterns:
            if pattern in lowered:
                signals.append(finding_type)
                break
    return sorted(set(signals))


def detect_patch_high_risk_signals(diff: str, files_changed: list[str] | None = None) -> list[str]:
    lowered = diff.lower()
    files = files_changed or changed_files_from_diff(diff)
    joined_files = "\n".join(files).lower()
    signals: list[str] = []
    for finding_type, patterns in HIGH_RISK_PATTERNS.items():
        for pattern in patterns:
            if pattern in lowered or pattern in joined_files:
                signals.append(finding_type)
                break
    if "deploy" in joined_files or "production" in joined_files:
        signals.append("deployment_config")
    return sorted(set(signals))


def validate_patch_gate(diff: str, files_changed: list[str] | None = None) -> list[str]:
    return detect_patch_blocking_signals(diff, files_changed)


def validate_branch_creation(branch_name: str, current_branch: str | None, dirty: bool, allow_dirty: bool = False, reuse: bool = False, exists: bool = False) -> list[str]:
    failures: list[str] = []
    if branch_name in MAIN_BRANCHES:
        failures.append("target branch must not be main or master")
    if dirty and not allow_dirty:
        failures.append("working tree is dirty; pass --allow-dirty to create a branch anyway")
    if exists and not reuse:
        failures.append("target branch already exists; pass --reuse to use it")
    if current_branch is None:
        failures.append("current branch could not be determined")
    return failures


def validate_patch_apply(blocked: bool, risk_level: str, current_branch: str | None, write: bool, allow_high_risk: bool = False, allow_main: bool = False) -> list[str]:
    failures: list[str] = []
    if blocked:
        failures.append("patch gate is blocked")
    if not write:
        return failures
    if risk_level in {"high", "critical"} and not allow_high_risk:
        failures.append("high-risk patch requires --allow-high-risk")
    if current_branch in MAIN_BRANCHES and not allow_main:
        failures.append("applying on main/master requires --allow-main")
    return failures


def validate_patch_commit(blocked: bool, risk_level: str, current_branch: str | None, message: str | None, staged: bool, allow_high_risk: bool = False, allow_main: bool = False) -> list[str]:
    failures: list[str] = []
    if blocked:
        failures.append("patch gate is blocked")
    if not message or not message.strip():
        failures.append("commit message is required")
    if risk_level in {"high", "critical"} and not allow_high_risk:
        failures.append("high-risk patch requires --allow-high-risk")
    if current_branch in MAIN_BRANCHES and not allow_main:
        failures.append("committing on main/master requires --allow-main")
    if not staged:
        failures.append("no staged changes are available to commit")
    return failures


def _added_lines(diff: str) -> list[str]:
    return [line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++")]
