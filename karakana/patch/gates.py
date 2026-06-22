"""Patch gate checks for captured patch artifacts."""

from __future__ import annotations

import json
import secrets
from fnmatch import fnmatch
from datetime import datetime, timezone
from pathlib import Path

from karakana.codex.schemas import PatchArtifact, PatchReview
from karakana.patch.schemas import PatchGateResult
from karakana.safety.patch import detect_patch_blocking_signals, detect_patch_high_risk_signals
from karakana.traces.schemas import redact_value


def run_patch_gate(repo_root: Path, patch_run_id: str, skillpack_context=None) -> tuple[PatchGateResult, Path]:
    patch_root = repo_root / ".karakana" / "patches" / patch_run_id
    checks_passed: list[str] = []
    checks_failed: list[str] = []
    warnings: list[str] = []
    required_actions: list[str] = []
    metadata: dict = {"patch_root": str(patch_root)}
    artifact = _load_patch_artifact(patch_root)
    diff_path = Path(artifact.diff_path) if artifact and artifact.diff_path else patch_root / "changes.diff"
    diff = ""
    if patch_root.exists():
        checks_passed.append("patch_exists")
    else:
        checks_failed.append("patch_exists")
    if diff_path.exists():
        checks_passed.append("diff_exists")
        diff = diff_path.read_text(encoding="utf-8")
    else:
        checks_failed.append("diff_exists")
    review, review_id = find_patch_review(repo_root, patch_run_id)
    if review:
        checks_passed.append("patch_review_exists")
        metadata["patch_review_status"] = review.status
        metadata["patch_review_blocked"] = review.blocked
        if review.blocked:
            checks_failed.append("patch_review_not_blocked")
        else:
            checks_passed.append("patch_review_not_blocked")
    else:
        checks_failed.append("patch_review_exists")
        required_actions.append(f"Run `karakana codex review-patch --diff {diff_path}`.")
    files_changed = artifact.files_changed if artifact else []
    blocking = detect_patch_blocking_signals(diff, files_changed)
    high_risk = detect_patch_high_risk_signals(diff, files_changed)
    skillpack_blocked = _matching_paths(files_changed, skillpack_context.blocked_paths if skillpack_context else [])
    skillpack_high_risk = _matching_paths(files_changed, skillpack_context.high_risk_paths if skillpack_context else [])
    if skillpack_blocked:
        blocking.append("skillpack_blocked_path")
    if skillpack_high_risk:
        high_risk.append("skillpack_high_risk_path")
    if skillpack_context:
        metadata["skillpack"] = skillpack_context.skillpack.name
        metadata["skillpack_blocked_paths"] = skillpack_blocked
        metadata["skillpack_high_risk_paths"] = skillpack_high_risk
    metadata.update({"blocking_signals": blocking, "high_risk_signals": high_risk, "files_changed": files_changed})
    for signal in blocking:
        checks_failed.append(f"no_{signal}")
    if not blocking:
        checks_passed.extend(["no_secret_findings", "no_env_exposure", "no_destructive_commands", "no_production_deploy"])
    test_evidence = load_test_evidence(repo_root, patch_run_id)
    metadata["test_evidence"] = test_evidence
    if _tests_present(test_evidence) or _docs_only(files_changed):
        checks_passed.append("tests_present_or_justified")
    else:
        warnings.append("No test evidence is attached for source changes.")
        required_actions.append(f"Attach tests with `karakana patch attach-test --patch-run {patch_run_id} --test-run <test-run-id>`.")
    if artifact and artifact.git_status is not None:
        checks_passed.append("working_tree_state_known")
    else:
        warnings.append("Working tree state is not known.")
    if artifact and artifact.git_branch:
        checks_passed.append("branch_state_known")
        metadata["git_branch"] = artifact.git_branch
    else:
        warnings.append("Branch state is not known.")
    if artifact:
        metadata.update(
            {
                "project": artifact.project,
                "skillpack": artifact.skillpack or metadata.get("skillpack"),
                "repository_path": artifact.repository_path,
            }
        )
    review_risk = review.risk_level if review else "medium"
    risk_level = _max_risk([review_risk, "high" if high_risk else "low", "critical" if blocking else "low"])
    if risk_level in {"high", "critical"}:
        warnings.append("High-risk patch requires --allow-high-risk before apply or commit.")
        required_actions.append("Request human review before applying.")
    else:
        checks_passed.append("risk_level_acceptable")
    blocked = bool(checks_failed and any(check in checks_failed for check in ("patch_exists", "diff_exists", "patch_review_not_blocked", "patch_review_exists")) or blocking or (review.blocked if review else False))
    status = "blocked" if blocked else ("warning" if warnings or risk_level in {"high", "critical"} else "passed")
    result = PatchGateResult(
        patch_run_id=patch_run_id,
        status=status,
        risk_level=risk_level,
        blocked=blocked,
        checks_passed=sorted(set(checks_passed)),
        checks_failed=sorted(set(checks_failed)),
        warnings=sorted(set(warnings)),
        required_actions=sorted(set(required_actions)),
        patch_review_id=review_id,
        metadata=metadata,
    )
    gate_dir = repo_root / ".karakana" / "patch-gates" / generate_gate_run_id()
    gate_dir.mkdir(parents=True, exist_ok=True)
    (gate_dir / "gate.json").write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (gate_dir / "gate.md").write_text(render_gate_markdown(result), encoding="utf-8")
    return result, gate_dir / "gate.json"


def find_patch_review(repo_root: Path, patch_run_id: str) -> tuple[PatchReview | None, str | None]:
    review_root = repo_root / ".karakana" / "patch-reviews"
    if not review_root.exists():
        return None, None
    matches: list[tuple[str, PatchReview]] = []
    for path in review_root.iterdir():
        review_json = path / "review.json"
        if not review_json.exists():
            continue
        data = json.loads(review_json.read_text(encoding="utf-8"))
        if data.get("patch_run_id") == patch_run_id:
            matches.append((path.name, PatchReview.from_dict(data)))
    if not matches:
        return None, None
    review_id, review = sorted(matches, key=lambda item: item[0], reverse=True)[0]
    return review, review_id


def load_test_evidence(repo_root: Path, patch_run_id: str) -> dict | None:
    path = repo_root / ".karakana" / "patches" / patch_run_id / "test-evidence.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def attach_test_evidence(repo_root: Path, patch_run_id: str, test_run_id: str) -> Path:
    test_root = repo_root / ".karakana" / "test-runs" / test_run_id
    result_path = test_root / "result.json"
    if not result_path.exists():
        raise FileNotFoundError(f"Test run not found: {test_run_id}")
    data = json.loads(result_path.read_text(encoding="utf-8"))
    evidence = {
        "patch_run_id": patch_run_id,
        "test_run_id": test_run_id,
        "result_path": str(result_path),
        "exit_code": data.get("exit_code"),
        "refused": data.get("refused"),
        "warnings": data.get("warnings", []),
    }
    output = repo_root / ".karakana" / "patches" / patch_run_id / "test-evidence.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(redact_value(evidence), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def render_gate_markdown(result: PatchGateResult) -> str:
    return f"""# Karakana Patch Gate

## Summary

- Patch run ID: {result.patch_run_id}
- Status: {result.status}
- Risk level: {result.risk_level}
- Blocked: {result.blocked}
- Patch review ID: {result.patch_review_id or ""}

## Checks Passed

{_bullets(result.checks_passed)}

## Checks Failed

{_bullets(result.checks_failed)}

## Warnings

{_bullets(result.warnings)}

## Required Actions

{_bullets(result.required_actions)}
"""


def _load_patch_artifact(patch_root: Path) -> PatchArtifact | None:
    path = patch_root / "patch.json"
    if not path.exists():
        return None
    return PatchArtifact.from_dict(json.loads(path.read_text(encoding="utf-8")))


def _tests_present(evidence: dict | None) -> bool:
    return bool(evidence and evidence.get("exit_code") == 0 and not evidence.get("refused"))


def _docs_only(files: list[str]) -> bool:
    return bool(files) and all(path.endswith(".md") or path.startswith("docs/") for path in files)


def _max_risk(values: list[str]) -> str:
    order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    return max(values, key=lambda item: order.get(item, 0))


def _matching_paths(files: list[str], patterns: list[str]) -> list[str]:
    matches: list[str] = []
    for path in files:
        for pattern in patterns:
            if fnmatch(path, pattern):
                matches.append(path)
                break
    return sorted(set(matches))


def generate_gate_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-gate-{secrets.token_hex(3)}"


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)
