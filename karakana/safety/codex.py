"""Safety helpers for Codex handoff and patch workflows."""

from __future__ import annotations

from pathlib import Path
import re

SECRET_PATTERNS = (
    "token",
    "secret",
    "password",
    "api_key",
    "apikey",
    "authorization",
    "bearer",
    "private_key",
    "client_secret",
    "access_key",
    "refresh_token",
)

DESTRUCTIVE_PATTERNS = (
    "rm -rf",
    "drop database",
    "kubectl delete",
    "terraform destroy",
    "git reset --hard",
    "git clean -fd",
    "delete all",
)

DEPLOY_PATTERNS = ("deploy", "kubectl apply", "helm upgrade", "docker push")
WRITE_GIT_PATTERNS = ("git push", "git commit", "gh pr create", "auto-merge")


def validate_codex_execution_request(
    explicit_execution: bool,
    current_branch: str | None,
    task_file: Path,
    output_dir: Path,
    repo_root: Path,
) -> list[str]:
    warnings: list[str] = []
    if not explicit_execution:
        warnings.append("Codex execution requires explicit --execute.")
    if current_branch in {"main", "master"}:
        warnings.append("Codex execution is refused on main/master.")
    if not task_file.exists():
        warnings.append(f"Task file does not exist: {task_file}")
    else:
        text = task_file.read_text(encoding="utf-8")
        if detect_secret_like_content(text):
            warnings.append("Task file appears to contain secret-like content.")
        if any(pattern in text.lower() for pattern in DEPLOY_PATTERNS):
            warnings.append("Task file appears to request deployment.")
    if not _under_karakana(output_dir, repo_root):
        warnings.append("Output directory must be under .karakana/.")
    return warnings


def validate_test_command(command: str) -> list[str]:
    warnings: list[str] = []
    if not command.strip():
        warnings.append("Test command must not be empty.")
    if detect_destructive_command(command):
        warnings.append("Command appears destructive.")
    lowered = command.lower()
    if any(pattern in lowered for pattern in DEPLOY_PATTERNS):
        warnings.append("Deployment commands are not allowed for test capture.")
    if any(pattern in lowered for pattern in WRITE_GIT_PATTERNS):
        warnings.append("Git write commands are not allowed for test capture.")
    if "cat .env" in lowered or "printenv" in lowered:
        warnings.append("Commands must not expose environment or .env content.")
    return warnings


def detect_destructive_command(command: str) -> bool:
    lowered = command.lower()
    return any(pattern in lowered for pattern in DESTRUCTIVE_PATTERNS)


def detect_secret_like_content(text: str) -> bool:
    return any(re.search(rf"\b{re.escape(term)}\s*[:=]\s*\S+", text, flags=re.IGNORECASE) for term in SECRET_PATTERNS)


def _under_karakana(path: Path, repo_root: Path) -> bool:
    try:
        resolved = path.resolve()
        root = (repo_root / ".karakana").resolve()
        return resolved == root or resolved.is_relative_to(root)
    except OSError:
        return False
