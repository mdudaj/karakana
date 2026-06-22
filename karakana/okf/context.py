"""Select bounded OKF concept context for agent tasks."""

from __future__ import annotations

from collections import deque
from pathlib import Path

from karakana.okf.schemas import OkfConcept
from karakana.okf.validator import OkfValidator

STATUS_PRIORITY = {"active": 0, "proposed": 1, "draft": 2, "runtime-evidence": 3, "superseded": 4, "deprecated": 5}


def select_concepts(
    repo_root: Path,
    *,
    project: str | None = None,
    concept_types: set[str] | None = None,
    tags: set[str] | None = None,
    statuses: set[str] | None = None,
    relationship_depth: int = 1,
    limit: int = 20,
) -> list[OkfConcept]:
    result = OkfValidator(repo_root).validate()
    if not result.ok:
        return []
    concepts_by_id = {concept.concept_id: concept for concept in result.concepts if concept.concept_id}
    selected = [
        concept
        for concept in result.concepts
        if _matches(concept, project=project, concept_types=concept_types, tags=tags, statuses=statuses)
    ]

    selected_ids = {concept.concept_id for concept in selected}
    queue = deque((concept.concept_id, 0) for concept in selected if concept.concept_id)
    while queue:
        concept_id, depth = queue.popleft()
        if depth >= relationship_depth:
            continue
        concept = concepts_by_id.get(concept_id)
        if concept is None:
            continue
        for related_ids in concept.relationships.values():
            for related_id in related_ids:
                if related_id not in selected_ids and related_id in concepts_by_id:
                    selected_ids.add(related_id)
                    queue.append((related_id, depth + 1))

    expanded = [concepts_by_id[concept_id] for concept_id in selected_ids if concept_id in concepts_by_id]
    return sorted(expanded, key=_sort_key)[:limit]


def _matches(
    concept: OkfConcept,
    *,
    project: str | None,
    concept_types: set[str] | None,
    tags: set[str] | None,
    statuses: set[str] | None,
) -> bool:
    if project and concept.project != project:
        return False
    if concept_types and concept.concept_type not in concept_types:
        return False
    if tags and not tags.intersection(concept.tags):
        return False
    if statuses and concept.status not in statuses:
        return False
    if not statuses and concept.status == "deprecated":
        return False
    return True


def _sort_key(concept: OkfConcept) -> tuple[int, str]:
    return (STATUS_PRIORITY.get(concept.status, 99), concept.concept_id)
