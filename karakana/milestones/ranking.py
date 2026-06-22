"""Transparent evidence relevance and multi-criteria milestone ranking."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from karakana.milestones.schemas import DecisionCriterion, MilestoneCandidate, SensitivityAnalysis


STOPWORDS = {
    "about", "after", "before", "better", "current", "from", "have", "implemented", "into", "need",
    "project", "reports", "should", "state", "that", "their", "there", "these", "this", "through", "users",
    "with", "without", "would", "could", "using", "used", "status",
}

DEFAULT_CRITERIA = (
    DecisionCriterion("blocker_priority", 0.25, "Whether the option resolves or safely avoids active blockers."),
    DecisionCriterion("user_alignment", 0.20, "Alignment with explicit user-reported needs and requested outcomes."),
    DecisionCriterion("evidence_strength", 0.15, "Strength and relevance of inspected project evidence."),
    DecisionCriterion("readiness", 0.15, "Planning, dependency, and verification readiness."),
    DecisionCriterion("risk_control", 0.10, "Ability to control unsafe or costly failure modes."),
    DecisionCriterion("reversibility", 0.10, "Ease of rollback or learning without lock-in."),
    DecisionCriterion("cost_efficiency", 0.05, "Expected value relative to implementation effort."),
)


@dataclass(frozen=True)
class RelevanceResult:
    score: float
    label: str
    matched_terms: list[str]


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for raw in re.findall(r"[a-z0-9]+", text.lower()):
        if len(raw) <= 3 or raw in STOPWORDS:
            continue
        token = raw
        if token.endswith("ies") and len(token) > 5:
            token = token[:-3] + "y"
        elif token.endswith("s") and not token.endswith("ss") and len(token) > 4:
            token = token[:-1]
        tokens.append(token)
    return tokens


def bm25_relevance(query: str | None, text: str, corpus: list[str]) -> RelevanceResult:
    """Return a normalized BM25-style score plus query coverage.

    This is a deterministic ranking signal, not a probability of relevance.
    """
    if not query:
        return RelevanceResult(0.5, "medium", [])
    query_terms = list(dict.fromkeys(tokenize(query)))
    document = tokenize(text)
    if not query_terms or not document:
        return RelevanceResult(0.0, "irrelevant", [])
    documents = [tokenize(item) for item in corpus if tokenize(item)] or [document]
    frequencies = Counter(document)
    average_length = sum(len(item) for item in documents) / len(documents)
    raw_score = 0.0
    matched: list[str] = []
    k1 = 1.2
    b = 0.75
    for term in query_terms:
        term_frequency = frequencies[term]
        if not term_frequency:
            continue
        matched.append(term)
        document_frequency = sum(1 for item in documents if term in item)
        inverse_document_frequency = math.log(1 + (len(documents) - document_frequency + 0.5) / (document_frequency + 0.5))
        denominator = term_frequency + k1 * (1 - b + b * len(document) / max(average_length, 1.0))
        raw_score += inverse_document_frequency * (term_frequency * (k1 + 1) / denominator)
    coverage = len(matched) / len(query_terms)
    saturation = raw_score / (raw_score + 3.0) if raw_score else 0.0
    score = round(0.7 * saturation + 0.3 * coverage, 4)
    if score >= 0.55:
        label = "high"
    elif score >= 0.35:
        label = "medium"
    elif score >= 0.18:
        label = "low"
    else:
        label = "irrelevant"
    return RelevanceResult(score, label, sorted(matched))


def focused_candidate_relevance(title: RelevanceResult, content: RelevanceResult) -> bool:
    """Require topical focus, not merely incidental terms in long candidate content."""
    return title.label in {"medium", "high"} or content.label == "high"


def rank_candidates(
    candidates: list[dict],
    criteria: tuple[DecisionCriterion, ...] = DEFAULT_CRITERIA,
) -> tuple[list[MilestoneCandidate], SensitivityAnalysis]:
    ranked = _score_candidates(candidates, {item.name: item.weight for item in criteria})
    sensitivity = _sensitivity(candidates, criteria, ranked)
    return ranked, sensitivity


def _score_candidates(candidates: list[dict], weights: dict[str, float]) -> list[MilestoneCandidate]:
    scored: list[tuple[float, dict]] = []
    for candidate in candidates:
        score = sum(weights[name] * candidate["criterion_scores"][name] for name in weights)
        scored.append((score, candidate))
    scored.sort(key=lambda item: (-item[0], item[1]["title"]))
    total = sum(score for score, _ in scored) or 1.0
    results = [
        MilestoneCandidate(
            title=item["title"],
            category=item["category"],
            decision_weight=round(score / total, 4),
            decision_score=round(score, 4),
            rationale=item["rationale"],
            risks=item["risks"],
            cost=item["cost"],
            reversibility=item["reversibility"],
            criterion_scores=dict(item["criterion_scores"]),
        )
        for score, item in scored
    ]
    if results:
        residual = round(1.0 - sum(item.decision_weight for item in results), 4)
        last = results[-1]
        results[-1] = MilestoneCandidate(
            title=last.title,
            category=last.category,
            decision_weight=round(last.decision_weight + residual, 4),
            decision_score=last.decision_score,
            rationale=last.rationale,
            risks=last.risks,
            cost=last.cost,
            reversibility=last.reversibility,
            criterion_scores=last.criterion_scores,
        )
    return results


def _sensitivity(
    candidates: list[dict],
    criteria: tuple[DecisionCriterion, ...],
    baseline: list[MilestoneCandidate],
) -> SensitivityAnalysis:
    scenarios: list[tuple[str, dict[str, float]]] = []
    base_weights = {item.name: item.weight for item in criteria}
    for criterion in criteria:
        without = {name: weight for name, weight in base_weights.items() if name != criterion.name}
        scenarios.append((f"drop:{criterion.name}", _normalize(without)))
        for factor in (0.8, 1.2):
            perturbed = dict(base_weights)
            perturbed[criterion.name] *= factor
            scenarios.append((f"{factor:.1f}x:{criterion.name}", _normalize(perturbed)))
    winner_counts: Counter[str] = Counter()
    critical: set[str] = set()
    for label, weights in scenarios:
        winner = _score_candidates(candidates, weights)[0].title
        winner_counts[winner] += 1
        if winner != baseline[0].title:
            critical.add(label.split(":", 1)[1])
    baseline_margin = baseline[0].decision_score - baseline[1].decision_score if len(baseline) > 1 else baseline[0].decision_score
    alternate_winners = sorted(title for title in winner_counts if title != baseline[0].title)
    return SensitivityAnalysis(
        method="leave-one-criterion-out plus +/-20% single-weight perturbation",
        scenarios_tested=len(scenarios),
        baseline_winner=baseline[0].title,
        baseline_margin=round(baseline_margin, 4),
        robust=not alternate_winners,
        winner_counts=dict(sorted(winner_counts.items())),
        alternate_winners=alternate_winners,
        critical_criteria=sorted(critical),
    )


def _normalize(weights: dict[str, float]) -> dict[str, float]:
    total = sum(weights.values()) or 1.0
    return {name: weight / total for name, weight in weights.items()}
