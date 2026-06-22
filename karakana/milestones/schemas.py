"""Schemas for next-milestone decision artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from karakana.traces.schemas import redact_value


@dataclass(frozen=True)
class MilestoneEvidence:
    source_type: str
    source_id: str | None
    path: str | None
    summary: str
    relevance: str = "high"
    relevance_score: float = 1.0
    matched_terms: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass(frozen=True)
class MilestoneCandidate:
    title: str
    category: str
    decision_weight: float
    decision_score: float
    rationale: str
    risks: str
    cost: str
    reversibility: str
    criterion_scores: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass(frozen=True)
class DecisionCriterion:
    name: str
    weight: float
    description: str

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass(frozen=True)
class SensitivityAnalysis:
    method: str
    scenarios_tested: int
    baseline_winner: str
    baseline_margin: float
    robust: bool
    winner_counts: dict[str, int] = field(default_factory=dict)
    alternate_winners: list[str] = field(default_factory=list)
    critical_criteria: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


@dataclass
class NextMilestoneDecision:
    run_id: str
    created_at: str
    workspace: str | None
    project: str
    skillpack: str
    current_state_summary: str
    evidence: list[MilestoneEvidence]
    open_findings: list[str]
    criteria: list[DecisionCriterion]
    candidates: list[MilestoneCandidate]
    sensitivity: SensitivityAnalysis
    recommended_milestone: str
    decision_rationale: str
    rejected_alternatives: list[str]
    generated_instructions: str
    verification_plan: list[str]
    definition_of_done: list[str]
    safety_notes: list[str]
    brainstorm_used: bool = True
    blocked: bool = False
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))
