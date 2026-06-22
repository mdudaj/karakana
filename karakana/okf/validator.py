"""Validate Karakana OKF concept bundles."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from karakana.okf.parser import OkfParseError, parse_concept_file
from karakana.okf.schemas import (
    ALLOWED_CONCEPT_TYPES,
    ALLOWED_STATUSES,
    BLOCKED_SOURCE_PATTERNS,
    REQUIRED_FIELDS,
    OkfConcept,
    OkfIssue,
    OkfValidationResult,
)


class OkfValidator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def validate(
        self,
        path: Path | None = None,
        *,
        strict: bool = False,
        allow_unknown_types: bool = False,
    ) -> OkfValidationResult:
        target = path or self.repo_root / "okf"
        result = OkfValidationResult(path=target)
        concept_paths = list(self._concept_paths(target))
        if not concept_paths:
            result.errors.append(OkfIssue(target, "No OKF concept markdown files found"))
            return result

        for concept_path in concept_paths:
            try:
                concept = parse_concept_file(concept_path)
            except OkfParseError as exc:
                result.errors.append(OkfIssue(concept_path, str(exc)))
                continue
            result.concepts.append(concept)
            self._validate_concept(concept, result, allow_unknown_types=allow_unknown_types)

        self._validate_relationships(result)
        self._count(result)
        if strict:
            result.errors.extend(result.warnings)
            result.warnings = []
        return result

    def _concept_paths(self, target: Path) -> Iterable[Path]:
        resolved = target if target.is_absolute() else self.repo_root / target
        if resolved.is_file():
            if resolved.suffix == ".md":
                yield resolved
            return
        if not resolved.exists():
            return
        yield from sorted(path for path in resolved.rglob("*.md") if path.is_file())

    def _validate_concept(self, concept: OkfConcept, result: OkfValidationResult, *, allow_unknown_types: bool) -> None:
        metadata = concept.metadata
        for field in REQUIRED_FIELDS:
            if field not in metadata or metadata[field] in (None, ""):
                result.errors.append(OkfIssue(concept.path, f"Missing required field: {field}"))

        concept_type = metadata.get("type")
        if concept_type and concept_type not in ALLOWED_CONCEPT_TYPES and not allow_unknown_types:
            result.errors.append(OkfIssue(concept.path, f"Unknown type: {concept_type}"))

        status = metadata.get("status")
        if status and status not in ALLOWED_STATUSES:
            result.errors.append(OkfIssue(concept.path, f"Invalid status: {status}"))

        tags = metadata.get("tags")
        if "tags" in metadata and not _string_list(tags):
            result.errors.append(OkfIssue(concept.path, "tags must be a list of strings"))

        concept_id = metadata.get("id")
        if concept_id and not isinstance(concept_id, str):
            result.errors.append(OkfIssue(concept.path, "id must be a string"))
        elif concept_id and "." not in concept_id:
            result.errors.append(OkfIssue(concept.path, "id must be a dotted identifier"))

        project = metadata.get("project")
        if isinstance(concept_id, str) and isinstance(project, str) and project != "global":
            if not concept_id.startswith(f"{project}."):
                result.errors.append(OkfIssue(concept.path, f"id must start with project prefix '{project}.'"))

        source = metadata.get("source")
        if isinstance(source, str):
            self._validate_source(concept.path, source, result)
        elif "source" in metadata:
            result.errors.append(OkfIssue(concept.path, "source must be a string"))

        relationships = metadata.get("relationships")
        if relationships is not None and not isinstance(relationships, dict):
            result.errors.append(OkfIssue(concept.path, "relationships must be a mapping"))
        elif isinstance(relationships, dict):
            for key, value in relationships.items():
                if not isinstance(key, str) or not _string_list(value):
                    result.errors.append(OkfIssue(concept.path, "relationships entries must be lists of strings"))

    def _validate_source(self, concept_path: Path, source: str, result: OkfValidationResult) -> None:
        normalized = source.replace("\\", "/").lstrip("/")
        if any(normalized == pattern or normalized.startswith(pattern) for pattern in BLOCKED_SOURCE_PATTERNS):
            result.errors.append(OkfIssue(concept_path, f"Blocked source path: {source}"))
            return
        if "://" in source:
            return
        source_path = self.repo_root / source
        if not source_path.exists():
            result.warnings.append(OkfIssue(concept_path, f"Source path does not exist: {source}"))

    @staticmethod
    def _validate_relationships(result: OkfValidationResult) -> None:
        concept_ids = {concept.concept_id for concept in result.concepts if concept.concept_id}
        for concept in result.concepts:
            for relation_targets in concept.relationships.values():
                for target in relation_targets:
                    if target not in concept_ids:
                        result.warnings.append(OkfIssue(concept.path, f"Unresolved relationship target: {target}"))

    @staticmethod
    def _count(result: OkfValidationResult) -> None:
        for concept in result.concepts:
            if concept.concept_type:
                result.counts_by_type[concept.concept_type] = result.counts_by_type.get(concept.concept_type, 0) + 1
            if concept.project:
                result.counts_by_project[concept.project] = result.counts_by_project.get(concept.project, 0) + 1


def _string_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)
