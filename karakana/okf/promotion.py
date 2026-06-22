"""Promotion records and proposals for durable OKF concepts."""

from __future__ import annotations

import re
import secrets
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

from karakana.okf.schemas import BLOCKED_SOURCE_PATTERNS
from karakana.okf.validator import OkfValidator

PROMOTION_REQUIRED_FIELDS = ["source_artifact", "concept_id", "reason", "reviewer", "date", "verification"]


@dataclass(frozen=True)
class PromotionValidationResult:
    path: Path
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class PromotionCandidate:
    source_artifact: str
    eligible: bool
    suggested_type: str
    project: str
    reason: str
    concept_id: str
    required_review: str = "human"


@dataclass(frozen=True)
class PromotionProposal:
    proposal_id: str
    directory: Path
    concept_path: Path
    promotion_record_path: Path
    candidate: PromotionCandidate


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


def scan_promotion_candidates(repo_root: Path, paths: list[Path] | None = None, project: str = "karakana") -> list[PromotionCandidate]:
    scan_paths = paths or _default_scan_paths(repo_root)
    candidates: list[PromotionCandidate] = []
    for path in scan_paths:
        resolved = path if path.is_absolute() else repo_root / path
        if resolved.is_dir():
            for child in sorted(resolved.rglob("*")):
                if child.is_file():
                    candidates.append(classify_promotion_candidate(repo_root, child, project=project))
        elif resolved.exists():
            candidates.append(classify_promotion_candidate(repo_root, resolved, project=project))
        else:
            candidates.append(
                PromotionCandidate(
                    source_artifact=str(path),
                    eligible=False,
                    suggested_type="RuntimeEvidence",
                    project=project,
                    reason="Source artifact does not exist.",
                    concept_id=f"{project}.missing.{_slug(path.name or 'artifact')}",
                )
            )
    return candidates


def classify_promotion_candidate(repo_root: Path, path: Path, project: str = "karakana") -> PromotionCandidate:
    source_artifact = _relative(repo_root, path)
    normalized = source_artifact.replace("\\", "/").lstrip("/")
    if any(normalized == pattern or normalized.startswith(pattern) for pattern in BLOCKED_SOURCE_PATTERNS):
        return _candidate(source_artifact, False, "RuntimeEvidence", project, "Blocked source path.")
    if ".karakana/traces/" in normalized or normalized.startswith(".karakana/traces/"):
        return _candidate(source_artifact, False, "RuntimeEvidence", project, "Raw traces are runtime evidence and are not promotable by default.")
    if ".karakana/eval-runs/" in normalized or normalized.startswith(".karakana/eval-runs/"):
        return _candidate(source_artifact, False, "RuntimeEvidence", project, "Eval run logs are runtime evidence and require lesson extraction first.")
    if normalized.startswith("docs/adr/") and path.suffix == ".md":
        return _candidate(source_artifact, True, "ADR", project, "ADR files are durable decisions.")
    if normalized.startswith(".karakana/requirements/") and path.name in {"prd.md", "stories.md"}:
        ready = _sibling_readiness_is_ready(path)
        return _candidate(source_artifact, ready, "Requirement" if path.name == "prd.md" else "UserStory", project, "Ready requirements and stories are promotable." if ready else "Requirement is not ready.")
    if "/schemas/" in f"/{normalized}" and path.suffix == ".json":
        return _candidate(source_artifact, True, "Schema", project, "Schema files are durable contracts.")
    if normalized.startswith(".karakana/handoffs/") and path.name == "handoff.md":
        return _candidate(source_artifact, True, "Handoff", project, "Handoffs can be promoted when they contain stable decisions or next actions.")
    return _candidate(source_artifact, False, "RuntimeEvidence", project, "No promotion rule matched.")


def write_promotion_proposal(repo_root: Path, artifact: Path, project: str = "karakana", reviewer: str = "REVIEW_REQUIRED") -> PromotionProposal:
    candidate = classify_promotion_candidate(repo_root, artifact if artifact.is_absolute() else repo_root / artifact, project=project)
    if not candidate.eligible:
        raise ValueError(f"Artifact is not eligible for promotion: {candidate.reason}")
    proposal_id = date.today().strftime("%Y%m%d") + f"-okf-proposal-{secrets.token_hex(3)}"
    directory = repo_root / ".karakana" / "okf-proposals" / proposal_id
    directory.mkdir(parents=True, exist_ok=False)
    concept_path = directory / "concept.md"
    promotion_record_path = directory / "promotion.yml"
    concept_path.write_text(_proposal_concept(candidate), encoding="utf-8")
    promotion_record_path.write_text(_promotion_record(candidate, reviewer), encoding="utf-8")
    validation = OkfValidator(repo_root).validate(concept_path, allow_unknown_types=False)
    if not validation.ok:
        raise ValueError("Generated proposal did not validate: " + "; ".join(issue.message for issue in validation.errors))
    return PromotionProposal(proposal_id, directory, concept_path, promotion_record_path, candidate)


def _default_scan_paths(repo_root: Path) -> list[Path]:
    return [
        repo_root / "docs" / "adr",
        repo_root / ".karakana" / "requirements",
        repo_root / ".karakana" / "handoffs",
        repo_root / "schemas",
    ]


def _candidate(source_artifact: str, eligible: bool, suggested_type: str, project: str, reason: str) -> PromotionCandidate:
    stem = Path(source_artifact).stem
    parent = Path(source_artifact).parent.name
    suffix = _slug(f"{parent}-{stem}")
    return PromotionCandidate(
        source_artifact=source_artifact,
        eligible=eligible,
        suggested_type=suggested_type,
        project=project,
        reason=reason,
        concept_id=f"{project}.promoted.{suffix}",
    )


def _sibling_readiness_is_ready(path: Path) -> bool:
    readiness = path.parent / "readiness.md"
    if not readiness.exists():
        return False
    text = readiness.read_text(encoding="utf-8").lower()
    return "ready: true" in text or "status: ready" in text


def _proposal_concept(candidate: PromotionCandidate) -> str:
    title = Path(candidate.source_artifact).stem.replace("-", " ").replace("_", " ").title()
    return f"""---
id: {candidate.concept_id}
type: {candidate.suggested_type}
title: {title}
status: proposed
owner: {candidate.project}
project: {candidate.project}
summary: Promotion proposal generated from {candidate.source_artifact}.
source: {candidate.source_artifact}
tags: [okf, promotion, {candidate.project}]
updated: {date.today().isoformat()}
---

# {title}

Promotion proposal generated from `{candidate.source_artifact}`.

Reason: {candidate.reason}
"""


def _promotion_record(candidate: PromotionCandidate, reviewer: str) -> str:
    payload = {
        "source_artifact": candidate.source_artifact,
        "concept_id": candidate.concept_id,
        "reason": candidate.reason,
        "reviewer": reviewer,
        "date": date.today().isoformat(),
        "verification": "karakana okf validate --strict",
        "required_review": candidate.required_review,
    }
    return yaml.safe_dump(payload, sort_keys=False)


def _relative(repo_root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "artifact"
