"""Markdown summaries for ingestion bundles."""

from __future__ import annotations

from karakana.ingestion.schemas import IngestionBundle, IngestionCandidate


def render_candidates_markdown(bundle: IngestionBundle) -> str:
    return f"""# Karakana Ingestion Candidates

## Ingestion

- Ingest ID: {bundle.ingest_id}
- Project: {bundle.project or ""}
- Skillpack: {bundle.skillpack or ""}
- Status: {bundle.status}
- Redaction applied: {bundle.redaction_applied}

## Sources

{_sources(bundle)}

## Classification Summary

{_classification(bundle)}

## Candidates

{_candidates(bundle.candidates)}

## Recommended Next Actions

{_bullets(bundle.next_actions)}
"""


def render_review_markdown(bundle: IngestionBundle, warnings: list[str], blocked: bool) -> str:
    return f"""# Karakana Ingestion Review

## Summary

- Ingest ID: {bundle.ingest_id}
- Status: {"blocked" if blocked else "ready_for_review"}
- Candidate count: {len(bundle.candidates)}
- Blocked: {blocked}

## Warnings

{_bullets(warnings)}

## Candidates

{_candidates(bundle.candidates)}

## Next Steps

- Review candidates manually.
- Run `karakana ingest apply {bundle.ingest_id}` for a dry run.
- Use `--write` only after human approval.
"""


def _sources(bundle: IngestionBundle) -> str:
    if not bundle.sources:
        return "- None"
    return "\n".join(f"- {source.source_type}: {source.title or source.source_id or source.path or ''}" for source in bundle.sources)


def _classification(bundle: IngestionBundle) -> str:
    if not bundle.candidates:
        return "- None"
    return "\n".join(f"- {candidate.candidate_id}: {candidate.classification.category if candidate.classification else candidate.candidate_type} ({candidate.risk_level})" for candidate in bundle.candidates)


def _candidates(candidates: list[IngestionCandidate]) -> str:
    if not candidates:
        return "- None"
    parts = []
    for candidate in candidates:
        rationale = candidate.classification.rationale if candidate.classification else ""
        parts.append(
            f"""### Candidate: {candidate.title}

- ID: {candidate.candidate_id}
- Type: {candidate.candidate_type}
- Target: {candidate.target_path or ""}
- Risk: {candidate.risk_level}
- Status: {candidate.status}
- Requires human review: {candidate.requires_human_review}

#### Summary

{candidate.summary}

#### Rationale

{rationale}

#### Evidence

{_bullets(candidate.evidence)}

#### Proposed Content

{candidate.proposed_content or ""}

#### Warnings

{_bullets(candidate.warnings)}
"""
        )
    return "\n\n".join(parts)


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)
