"""Generate reviewable ingestion candidates."""

from __future__ import annotations

import secrets

from karakana.ingestion.classifier import classify_content
from karakana.ingestion.schemas import IngestionCandidate, IngestionSource

TYPE_MAP = {
    "ubongo_memory": "ubongo_memory",
    "skill_update": "skill_update",
    "eval_update": "eval_update",
    "prompt_update": "prompt_update",
    "safety_update": "safety_update",
    "project_convention": "project_convention",
    "behavior_update": "behavior_update",
    "manual_review": "manual_review",
}


def generate_candidates(source: IngestionSource, content: str, project: str | None = None, skillpack_context=None) -> list[IngestionCandidate]:
    classification = classify_content(content, project=project, skillpack_context=skillpack_context)
    candidate_type = TYPE_MAP.get(classification.category, "manual_review")
    target = classification.suggested_targets[0] if classification.suggested_targets else None
    summary = _excerpt(content)
    proposed = _proposed_content(candidate_type, summary, source)
    return [
        IngestionCandidate(
            candidate_id=f"candidate-{secrets.token_hex(3)}",
            candidate_type=candidate_type,
            title=f"Proposed {candidate_type.replace('_', ' ')} from {source.source_type}",
            summary=summary,
            target_path=target,
            proposed_content=proposed,
            evidence=[source.path or source.source_id or source.source_type],
            classification=classification,
            risk_level=classification.risk_level,
            status="ready_for_review",
            warnings=classification.warnings,
        )
    ]


def _proposed_content(candidate_type: str, summary: str, source: IngestionSource) -> str:
    return f"\n\n## Candidate from {source.source_type}: {source.title or source.source_id or source.path or 'source'}\n\n{summary}\n"


def _excerpt(text: str, limit: int = 900) -> str:
    cleaned = text.strip()
    return cleaned if len(cleaned) <= limit else cleaned[: limit - 3].rstrip() + "..."
