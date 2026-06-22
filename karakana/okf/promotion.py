"""Promotion records for turning runtime evidence into durable OKF concepts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from karakana.okf.schemas import BLOCKED_SOURCE_PATTERNS

PROMOTION_REQUIRED_FIELDS = ["source_artifact", "concept_id", "reason", "reviewer", "date", "verification"]


@dataclass(frozen=True)
class PromotionValidationResult:
    path: Path
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_promotion_record(repo_root: Path, path: Path) -> PromotionValidationResult:
    resolved = path if path.is_absolute() else repo_root / path
    errors: list[str] = []
    warnings: list[str] = []
    if not resolved.exists():
        return PromotionValidationResult(path=resolved, errors=[f"Promotion record not found: {resolved}"], warnings=warnings)
    try:
        raw = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return PromotionValidationResult(path=resolved, errors=[f"Invalid YAML: {exc}"], warnings=warnings)
    if not isinstance(raw, dict):
        return PromotionValidationResult(path=resolved, errors=["Promotion record must be a mapping"], warnings=warnings)

    for field in PROMOTION_REQUIRED_FIELDS:
        if not raw.get(field):
            errors.append(f"Missing required field: {field}")

    source_artifact = raw.get("source_artifact")
    if isinstance(source_artifact, str):
        normalized = source_artifact.replace("\\", "/").lstrip("/")
        if any(normalized == pattern or normalized.startswith(pattern) for pattern in BLOCKED_SOURCE_PATTERNS):
            errors.append(f"Blocked source artifact: {source_artifact}")
        elif not (repo_root / source_artifact).exists():
            warnings.append(f"Source artifact does not exist: {source_artifact}")
    elif "source_artifact" in raw:
        errors.append("source_artifact must be a string")

    concept_id = raw.get("concept_id")
    if isinstance(concept_id, str) and "." not in concept_id:
        errors.append("concept_id must be a dotted identifier")
    elif "concept_id" in raw and not isinstance(concept_id, str):
        errors.append("concept_id must be a string")

    return PromotionValidationResult(path=resolved, errors=errors, warnings=warnings)
