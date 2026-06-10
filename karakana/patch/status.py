"""Patch lifecycle status summaries."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from karakana.codex.schemas import PatchArtifact
from karakana.patch.gates import find_patch_review, load_test_evidence, run_patch_gate
from karakana.tools.code_search import _git_branch
from karakana.traces.schemas import redact_value


def build_patch_status(repo_root: Path, patch_run_id: str) -> dict:
    patch_root = repo_root / ".karakana" / "patches" / patch_run_id
    artifact = _load_patch_artifact(patch_root)
    gate, gate_path = run_patch_gate(repo_root, patch_run_id)
    review, review_id = find_patch_review(repo_root, patch_run_id)
    test_evidence = load_test_evidence(repo_root, patch_run_id)
    status = {
        "patch_run_id": patch_run_id,
        "patch": artifact.to_dict() if artifact else None,
        "gate": gate.to_dict(),
        "gate_path": str(gate_path),
        "review": review.to_dict() if review else None,
        "patch_review_id": review_id,
        "test_evidence": test_evidence,
        "branch": {"current": _git_branch(repo_root)},
        "working_tree": {
            "status": _git(repo_root, ["status", "--short"]).stdout,
            "staged_files": _git(repo_root, ["diff", "--cached", "--name-only"]).stdout.splitlines(),
        },
        "apply_status": _latest_json(repo_root / ".karakana" / "patch-apply", patch_run_id),
        "commit_status": _latest_json(repo_root / ".karakana" / "patch-commits", patch_run_id),
        "recommended_next_actions": _next_actions(gate.blocked, gate.risk_level, bool(test_evidence)),
    }
    return redact_value(status)


def write_patch_status(repo_root: Path, patch_run_id: str) -> tuple[Path, dict]:
    data = build_patch_status(repo_root, patch_run_id)
    root = repo_root / ".karakana" / "patch-status" / patch_run_id
    root.mkdir(parents=True, exist_ok=True)
    json_path = root / "status.json"
    md_path = root / "status.md"
    json_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_patch_status(data), encoding="utf-8")
    return md_path, data


def render_patch_status(data: dict) -> str:
    gate = data.get("gate") or {}
    review = data.get("review") or {}
    patch = data.get("patch") or {}
    branch = data.get("branch") or {}
    working_tree = data.get("working_tree") or {}
    return f"""# Karakana Patch Status

## Patch

- Patch run ID: {data.get("patch_run_id")}
- Diff: {patch.get("diff_path") or ""}
- Files changed: {len(patch.get("files_changed") or [])}

## Gate

- Status: {gate.get("status") or ""}
- Risk level: {gate.get("risk_level") or ""}
- Blocked: {gate.get("blocked")}

## Review

- Patch review ID: {data.get("patch_review_id") or ""}
- Status: {review.get("status") or ""}
- Risk level: {review.get("risk_level") or ""}
- Blocked: {review.get("blocked")}

## Test Evidence

{_test_evidence(data.get("test_evidence"))}

## Branch

- Current branch: {branch.get("current") or ""}

## Working Tree

```text
{working_tree.get("status") or ""}
```

## Apply Status

{_dict_block(data.get("apply_status"))}

## Commit Status

{_dict_block(data.get("commit_status"))}

## Recommended Next Actions

{_bullets(data.get("recommended_next_actions") or [])}
"""


def _load_patch_artifact(patch_root: Path) -> PatchArtifact | None:
    path = patch_root / "patch.json"
    if not path.exists():
        return None
    return PatchArtifact.from_dict(json.loads(path.read_text(encoding="utf-8")))


def _latest_json(root: Path, patch_run_id: str) -> dict | None:
    if not root.exists():
        return None
    matches = []
    for path in root.iterdir():
        candidate = path / "result.json"
        if candidate.exists():
            data = json.loads(candidate.read_text(encoding="utf-8"))
            if data.get("patch_run_id") == patch_run_id:
                matches.append((path.name, data))
    if not matches:
        return None
    return sorted(matches, key=lambda item: item[0], reverse=True)[0][1]


def _next_actions(blocked: bool, risk_level: str, has_tests: bool) -> list[str]:
    if blocked:
        return ["Resolve blocking gate findings before apply or commit."]
    actions = []
    if risk_level in {"high", "critical"}:
        actions.append("Request human review and pass --allow-high-risk only after approval.")
    if not has_tests:
        actions.append("Attach relevant test evidence before commit.")
    actions.append("Use dry-run apply before any --write operation.")
    return actions


def _git(repo_root: Path, command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *command], cwd=repo_root, capture_output=True, text=True, check=False)


def _test_evidence(data: dict | None) -> str:
    if not data:
        return "- None"
    return f"- Test run ID: {data.get('test_run_id')}\n- Exit code: {data.get('exit_code')}\n- Result: {data.get('result_path')}"


def _dict_block(data: dict | None) -> str:
    if not data:
        return "- None"
    return "```json\n" + json.dumps(data, indent=2, sort_keys=True) + "\n```"


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)
