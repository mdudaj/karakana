"""Rule-based patch review."""

from __future__ import annotations

import json
import re
import secrets
from fnmatch import fnmatch
from datetime import datetime, timezone
from pathlib import Path

from karakana.codex.schemas import PatchReview, PatchReviewFinding
from karakana.models.router import route_model
from karakana.traces.schemas import redact_value

BLOCKING_PATTERNS = {
    "secret": ("token=", "password=", "client_secret=", "api_key=", "authorization: bearer", "private_key"),
    "env_file": ("cat .env", "print env", "show secrets"),
    "production_deploy": ("deploy to production", "kubectl apply", "helm upgrade", "docker push"),
    "destructive_command": ("rm -rf", "drop database", "git reset --hard", "terraform destroy"),
    "branch_protection_bypass": ("disable branch protection", "bypass branch protection"),
    "auto_merge": ("auto-merge", "gh pr merge --auto"),
}

HIGH_RISK_PATTERNS = {
    "auth_or_permission": ("auth", "permission", "oauth", "sso", "authorization"),
    "payment_or_billing": ("payment", "billing", "gepg", "reconciliation"),
    "database_migration": ("migration", "alembic", "schema", "database"),
    "opensearch_index": ("opensearch", "index"),
    "viewflow_process_state": ("viewflow", "process state", "workflow state", "transition"),
    "github_workflow": (".github/workflows",),
}


class PatchReviewer:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def review_diff(self, diff_path: Path, output_dir: Path | None = None, skillpack_context=None, project: str | None = None) -> Path:
        diff = diff_path.read_text(encoding="utf-8")
        patch_run_id = _patch_run_id_from_path(diff_path)
        patch_metadata = _patch_metadata(diff_path)
        review = review_patch_text(
            diff,
            patch_run_id=patch_run_id,
            skillpack_context=skillpack_context,
            project=project or patch_metadata.get("project"),
            skillpack=skillpack_context.skillpack.name if skillpack_context else patch_metadata.get("skillpack"),
            repository_path=patch_metadata.get("repository_path"),
        )
        root = _review_dir(self.repo_root, output_dir)
        root.mkdir(parents=True, exist_ok=True)
        (root / "evidence").mkdir(exist_ok=True)
        (root / "review.json").write_text(json.dumps(review.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (root / "review.md").write_text(render_patch_review(review, diff, skillpack_name=skillpack_context.skillpack.name if skillpack_context else None), encoding="utf-8")
        return root / "review.json"


def review_patch_text(diff: str, patch_run_id: str | None = None, skillpack_context=None, project: str | None = None, skillpack: str | None = None, repository_path: str | None = None) -> PatchReview:
    findings: list[PatchReviewFinding] = []
    files = changed_files_from_diff(diff)
    lowered = diff.lower()
    lowered_added_lines = "\n".join(_added_lines(diff)).lower()
    env_files = [path for path in files if Path(path).name == ".env" or Path(path).name.startswith(".env.")]
    if env_files:
        findings.append(PatchReviewFinding("env_file", "critical", "Patch modifies environment/credential file paths.", evidence=", ".join(env_files)))
    for finding_type, patterns in BLOCKING_PATTERNS.items():
        for pattern in patterns:
            if finding_type == "secret" and _only_redacted_secret_mentions(lowered_added_lines, pattern):
                continue
            if pattern in lowered_added_lines:
                findings.append(PatchReviewFinding(finding_type, "critical", f"Blocking pattern detected: {pattern}", evidence=pattern))
                break
    for finding_type, patterns in HIGH_RISK_PATTERNS.items():
        for pattern in patterns:
            if pattern in lowered:
                findings.append(PatchReviewFinding(finding_type, "high", f"High-risk patch area detected: {pattern}", evidence=pattern))
                break
    if skillpack_context:
        for path in _matching_paths(files, skillpack_context.blocked_paths):
            findings.append(PatchReviewFinding("skillpack_blocked_path", "critical", f"Skillpack blocked path changed: {path}", file_path=path))
        for path in _matching_paths(files, skillpack_context.high_risk_paths):
            findings.append(PatchReviewFinding("skillpack_high_risk_path", "high", f"Skillpack high-risk path changed: {path}", file_path=path))
    if len(files) > 5:
        findings.append(PatchReviewFinding("large_diff_size", "medium", "Patch changes more than five files."))
    source_files = [path for path in files if not _is_test_file(path) and not path.endswith(".md")]
    test_files = [path for path in files if _is_test_file(path)]
    if source_files and not test_files:
        findings.append(PatchReviewFinding("missing_tests", "medium", "Source changes are present without test file changes."))
    if test_files and not source_files:
        findings.append(PatchReviewFinding("test_without_source", "low", "Test files changed without source file changes."))
    blocked = any(finding.severity == "critical" for finding in findings)
    risk = _risk_level(findings)
    status = "blocked" if blocked else ("warning" if findings else "passed")
    return PatchReview(
        patch_run_id=patch_run_id or "unknown",
        status=status,
        risk_level=risk,
        findings=findings,
        blocked=blocked,
        recommended_next_actions=_next_actions(blocked, risk),
        project=project,
        skillpack=skillpack,
        repository_path=repository_path,
    )


def render_patch_review(review: PatchReview, diff: str, skillpack_name: str | None = None) -> str:
    files = changed_files_from_diff(diff)
    route = route_model(_route_type_for_review(review))
    return f"""# Karakana Patch Review

## Summary

- Patch review ID: {review.patch_run_id}
- Patch run ID: {review.patch_run_id}
- Status: {review.status}
- Risk level: {review.risk_level}
- Blocked: {review.blocked}
- Skillpack: {skillpack_name or review.skillpack or ""}
- Project: {review.project or ""}
- Repository: {review.repository_path or ""}

## Files Changed

{_bullets(files)}

## Findings

{_findings_markdown(review.findings)}

## Test Coverage Review

{_test_review(files)}

## Safety Review

Blocking findings prevent automatic publishing or handoff.

## Recommended Codex Model for Follow-up

- Provider: {route['provider']}
- Model: {route['model']}
- Rationale: {route.get('rationale')}

## Recommended Next Actions

{_bullets(review.recommended_next_actions)}

## Human Review Required

True
"""


def changed_files_from_diff(diff: str) -> list[str]:
    files = []
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            files.append(line.removeprefix("+++ b/"))
    return sorted(set(files))


def _added_lines(diff: str) -> list[str]:
    lines = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++") and "[REDACTED]" not in line:
            lines.append(line[1:])
    return lines


def _only_redacted_secret_mentions(text: str, pattern: str) -> bool:
    return pattern in text and "[redacted]" in text and text.count(pattern) == text.count("[redacted]")


def _review_dir(repo_root: Path, output_dir: Path | None) -> Path:
    if output_dir is None:
        return repo_root / ".karakana" / "patch-reviews" / generate_patch_review_id()
    path = output_dir if output_dir.is_absolute() else repo_root / output_dir
    resolved = path.resolve()
    root = (repo_root / ".karakana").resolve()
    if not (resolved == root or resolved.is_relative_to(root)):
        raise ValueError("Patch review output must be under .karakana/.")
    return path


def generate_patch_review_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-review-{secrets.token_hex(3)}"


def _patch_run_id_from_path(path: Path) -> str:
    return path.parent.name if path.parent.name else "unknown"


def _patch_metadata(diff_path: Path) -> dict:
    patch_json = diff_path.parent / "patch.json"
    if not patch_json.exists():
        return {}
    try:
        return json.loads(patch_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _is_test_file(path: str) -> bool:
    return "test" in Path(path).name or "/tests/" in path or path.startswith("tests/")


def _risk_level(findings: list[PatchReviewFinding]) -> str:
    if any(f.severity == "critical" for f in findings):
        return "critical"
    if any(f.severity == "high" for f in findings):
        return "high"
    if any(f.severity == "medium" for f in findings):
        return "medium"
    return "low"


def _route_type_for_review(review: PatchReview) -> str:
    if review.risk_level in {"critical", "high"}:
        return "high_risk_code_review"
    if review.risk_level == "medium":
        return "refactoring"
    return "routine_code_implementation"


def _next_actions(blocked: bool, risk: str) -> list[str]:
    if blocked:
        return ["Stop and inspect blocking safety findings.", "Do not publish or apply this patch automatically."]
    if risk in {"high", "critical"}:
        return ["Request senior human review.", "Consider GPT-5.5 follow-up review."]
    return ["Run relevant tests.", "Proceed only after human review."]


def _findings_markdown(findings: list[PatchReviewFinding]) -> str:
    if not findings:
        return "- None"
    return "\n\n".join(f"### {finding.severity}: {finding.finding_type}\n\n{finding.message}" for finding in findings)


def _test_review(files: list[str]) -> str:
    if any(_is_test_file(path) for path in files):
        return "Test files are present in the patch."
    return "No test files were detected in the patch."


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {redact_value(value)}" for value in values)


def _matching_paths(files: list[str], patterns: list[str]) -> list[str]:
    matches: list[str] = []
    for path in files:
        for pattern in patterns:
            if fnmatch(path, pattern):
                matches.append(path)
                break
    return sorted(set(matches))
