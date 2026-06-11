"""Generate v1 hardening backlog from dogfood findings."""

from __future__ import annotations

import secrets
from pathlib import Path

from karakana.dogfood.schemas import DogfoodBacklogItem, DogfoodFinding
from karakana.dogfood.summary import DogfoodStore


def generate_backlog(repo_root: Path, dogfood_id: str) -> tuple[list[DogfoodBacklogItem], Path]:
    store = DogfoodStore(repo_root)
    run = store.load(dogfood_id)
    items = [_item_from_finding(finding) for finding in run.findings]
    if not items:
        items.append(
            DogfoodBacklogItem(
                item_id=f"backlog-{secrets.token_hex(3)}",
                title="Repeat dogfood run with real workflow artifacts",
                item_type="manual_review",
                summary="No concrete findings were detected. Run the checklist with real action, patch, ingestion, and crosslink artifacts before release candidate.",
                priority="p2",
                acceptance_criteria=["A dogfood report includes exercised workflow artifacts.", "Manual review confirms no release blockers."],
                suggested_skills=["karakana-self-improvement"],
                recommended_model_route={"provider": "github", "model": "gpt-5-mini", "rationale": "Planning and review backlog triage."},
            )
        )
    run.backlog = items
    store.save(run)
    return items, store.run_dir(dogfood_id) / "backlog.md"


def _item_from_finding(finding: DogfoodFinding) -> DogfoodBacklogItem:
    priority = "p0" if finding.severity in {"high", "critical"} and finding.finding_type == "broken_command" else ("p1" if finding.severity in {"high", "critical"} else ("p2" if finding.severity == "medium" else "p3"))
    item_type = {
        "broken_command": "bug",
        "ux_friction": "ux_improvement",
        "missing_eval": "eval_update",
        "missing_doc": "doc_update",
        "weak_doc": "doc_update",
        "safety_gap": "safety_update",
        "routing_gap": "prompt_update",
        "trace_gap": "test_update",
        "artifact_gap": "test_update",
    }.get(finding.finding_type, "manual_review")
    return DogfoodBacklogItem(
        item_id=f"backlog-{secrets.token_hex(3)}",
        title=finding.title,
        item_type=item_type,
        summary=finding.summary,
        priority=priority,
        source_finding_ids=[finding.finding_id],
        suggested_issue_title=f"Dogfood: {finding.title}",
        suggested_skills=[finding.suggested_skill] if finding.suggested_skill else ["karakana-self-improvement"],
        acceptance_criteria=["Finding is reproduced or dismissed.", "Fix, doc update, eval, or safety refinement is reviewed.", "Relevant tests or evals pass."],
        recommended_model_route={"provider": "github", "model": "gpt-5-mini", "rationale": "Dogfood hardening triage and planning."},
        risk_level=finding.risk_level,
    )
