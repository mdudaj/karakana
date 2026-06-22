"""Safe dogfood runner."""

from __future__ import annotations

import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

from karakana.actions.extractor import ActionExtractor
from karakana.actions.store import ActionStore
from karakana.codex.handoff import CodexHandoffBuilder
from karakana.dogfood.checklist import CHECKLIST_TEMPLATE
from karakana.dogfood.schemas import DogfoodCommandResult
from karakana.dogfood.summary import DogfoodStore, new_dogfood_run
from karakana.models.review.report import write_review_artifacts
from karakana.models.review.schemas import ResponseReview
from karakana.traces.schemas import redact_value

SAFE_COMMANDS: dict[str, str] = {
    "version": "karakana version",
    "doctor": "karakana doctor",
    "config_validate": "karakana config validate",
    "release_check": "karakana release check",
    "workspace_status": "karakana workspace status --workspace default",
    "skill_validate_all": "karakana skill validate-all",
    "skillpack_validate_all": "karakana skillpack validate-all",
    "workspace_validate_all": "karakana workspace validate-all",
    "eval_run": "karakana eval run",
}

FULL_COMMAND_IDS = ["version", "doctor", "config_validate", "release_check", "workspace_status", "skill_validate_all", "skillpack_validate_all", "workspace_validate_all", "eval_run"]
DEFAULT_COMMAND_IDS = ["version", "doctor", "config_validate", "release_check", "workspace_status"]


def run_dogfood(repo_root: Path, project: str, skillpack: str | None, *, full: bool = False, command_id: str | None = None, dry_run: bool = False) -> tuple:
    command_ids = [command_id] if command_id else (FULL_COMMAND_IDS if full else DEFAULT_COMMAND_IDS)
    invalid = [item for item in command_ids if item not in SAFE_COMMANDS]
    if invalid:
        raise ValueError(f"Dogfood command is not allowlisted: {', '.join(invalid)}")
    store = DogfoodStore(repo_root)
    run = new_dogfood_run(project, skillpack, status="completed" if dry_run else "running")
    (store.run_dir(run.dogfood_id)).mkdir(parents=True, exist_ok=True)
    (store.run_dir(run.dogfood_id) / "checklist.md").write_text(CHECKLIST_TEMPLATE, encoding="utf-8")
    for item in command_ids:
        command = SAFE_COMMANDS[item]
        if dry_run:
            run.command_results.append(DogfoodCommandResult(command_id=item, command=command, status="planned"))
            continue
        run.command_results.append(_execute_allowlisted(repo_root, item, command))
    fixture_result = prepare_workflow_fixtures(repo_root, run.dogfood_id, project, skillpack)
    run.command_results.append(fixture_result)
    if not dry_run:
        if any(result.status in {"failed", "error"} for result in run.command_results):
            run.status = "failed"
        elif any(result.status == "warning" for result in run.command_results):
            run.status = "completed_with_warnings"
        else:
            run.status = "completed"
    path = store.save(run)
    return run, path


def _execute_allowlisted(repo_root: Path, command_id: str, command: str) -> DogfoodCommandResult:
    args = _command_args(repo_root, command)
    started = time.monotonic()
    try:
        result = subprocess.run(args, cwd=repo_root, text=True, capture_output=True, check=False, timeout=120)
    except Exception as exc:
        return DogfoodCommandResult(command_id=command_id, command=command, status="error", duration_seconds=round(time.monotonic() - started, 3), errors=[str(exc)])
    duration = round(time.monotonic() - started, 3)
    stdout = _redact_excerpt(result.stdout)
    stderr = _redact_excerpt(result.stderr)
    warning_lines = _significant_warning_lines(command_id, stdout, stderr)
    status = "passed" if result.returncode == 0 else "failed"
    if warning_lines and status == "passed":
        status = "warning"
    return DogfoodCommandResult(command_id=command_id, command=command, status=status, exit_code=result.returncode, stdout_excerpt=stdout, stderr_excerpt=stderr, duration_seconds=duration, noise_score=_noise_score(stdout, stderr), warnings=warning_lines, errors=[] if result.returncode == 0 else [stderr or stdout or f"exit={result.returncode}"])


def prepare_workflow_fixtures(repo_root: Path, dogfood_id: str, project: str, skillpack: str | None) -> DogfoodCommandResult:
    """Create local reviewable artifacts to exercise action extraction and Codex handoff."""
    artifact_dir = repo_root / ".karakana" / "dogfood" / dogfood_id / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    response_path = artifact_dir / "model-response.md"
    response_path.write_text(
        """# Dogfood Model Response Fixture

## Standards Review

Karakana should remain dry-run by default and preserve human review.

## Spec Review

Harden Karakana v1 release readiness using dogfood findings.

## Next Actions

- Codex task: Implement a documentation correction for the dogfood workflow, without executing Codex.
- Add eval: Add a regression case that verifies dogfood does not apply patches.
- Documentation: Update docs to clarify safe dogfood execution.

## Suggested Skills

- karakana-self-improvement
- karakana-handoff
""",
        encoding="utf-8",
    )
    write_review_artifacts(ResponseReview(status="passed", warnings=["Dogfood fixture; human review still required."]), artifact_dir)
    artifacts = [str(response_path), str(artifact_dir / "response-review.json")]
    try:
        bundle = ActionExtractor(repo_root).extract_from_response(response_path, project=project, skill=skillpack, require_passed_review=True)
        actions_path = ActionStore(repo_root).save(bundle)
        codex_paths = CodexHandoffBuilder(repo_root).build_from_action_bundle(bundle.action_run_id, project=project, skill=skillpack)
        artifacts.extend([str(actions_path), *[str(path) for path in codex_paths]])
    except Exception as exc:
        return DogfoodCommandResult(command_id="workflow_fixtures", command="dogfood prepare workflow fixtures", status="warning", artifact_paths=artifacts, stdout_excerpt="Prepared model response and review fixtures only.", warnings=[f"Action/Codex fixture generation skipped: {exc}"], noise_score=1)
    return DogfoodCommandResult(command_id="workflow_fixtures", command="dogfood prepare workflow fixtures", status="passed", artifact_paths=artifacts, stdout_excerpt="Prepared model response, response review, action bundle, and Codex handoff fixtures.", noise_score=0)


def _command_args(repo_root: Path, command: str) -> list[str]:
    parts = shlex.split(command)
    if parts and parts[0] == "karakana":
        binary = repo_root / ".venv" / "bin" / "karakana"
        if binary.exists():
            return [str(binary), *parts[1:]]
    if parts and parts[0] == "pytest":
        return [sys.executable, "-m", "pytest", *parts[1:]]
    return parts


def _redact_excerpt(text: str | None, limit: int = 1200) -> str:
    redacted = redact_value(text or "")
    redacted = re.sub(r"\b(GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY)\b", "[REDACTED_SECRET_NAME]", str(redacted))
    return redacted[:limit]


def _significant_warning_lines(command_id: str, stdout: str, stderr: str) -> list[str]:
    lines = [line.strip() for line in f"{stdout}\n{stderr}".splitlines() if line.strip()]
    warning_lines = [line for line in lines if _looks_like_warning(line)]
    return [line for line in warning_lines if not _is_informational_warning(command_id, line)]


def _looks_like_warning(line: str) -> bool:
    lowered = line.lower().strip()
    if lowered in {"warnings:", "warning:"}:
        return False
    if lowered.startswith("- none") or lowered in {"none", "no warnings", "warnings: none", "warning: none"}:
        return False
    return "warning" in lowered or lowered.startswith("- warning")


def _is_informational_warning(command_id: str, line: str) -> bool:
    if command_id != "doctor":
        return False
    lowered = line.lower()
    optional_credential_terms = (
        "github token",
        "github_token",
        "openai",
        "openai_api_key",
        "anthropic",
        "anthropic_api_key",
        "credential",
        "credentials",
    )
    missing_terms = ("missing", "not configured", "not set", "unavailable")
    return any(term in lowered for term in optional_credential_terms) and any(term in lowered for term in missing_terms)


def _noise_score(stdout: str, stderr: str) -> int:
    text = f"{stdout}\n{stderr}"
    lines = [line for line in text.splitlines() if line.strip()]
    warning_lines = [line for line in lines if "warning" in line.lower()]
    return min(100, len(lines) + (len(warning_lines) * 5))
