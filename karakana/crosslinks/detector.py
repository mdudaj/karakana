"""Deterministic cross-project pattern detection."""

from __future__ import annotations

import secrets
from collections import defaultdict

from karakana.crosslinks.schemas import CrosslinkEvidence, CrosslinkPattern, CrosslinkProjectRef

RISK_TERMS = {"auth", "authentication", "permission", "payment", "billing", "migration", "opensearch", "workflow", "viewflow", "process", "sso"}


def detect_patterns(projects: list[CrosslinkProjectRef], evidence: list[CrosslinkEvidence]) -> list[CrosslinkPattern]:
    patterns: list[CrosslinkPattern] = []
    patterns.extend(_shared_skills(projects))
    patterns.extend(_shared_tags(projects))
    patterns.extend(_shared_risks(projects, evidence))
    patterns.extend(_artifact_patterns(evidence))
    return patterns or [_pattern("manual_review", "No strong cross-project pattern detected", "Review selected projects manually.", [project.project_id for project in projects], evidence, ["docs/cross-project-notes.md"], "low", 0.2)]


def _shared_skills(projects: list[CrosslinkProjectRef]) -> list[CrosslinkPattern]:
    by_skill: dict[str, list[str]] = defaultdict(list)
    for project in projects:
        if project.skillpack:
            by_skill[project.skillpack].append(project.project_id)
    return [
        _pattern("shared_skill_need", f"Shared skillpack: {skill}", f"Multiple projects use `{skill}` and may benefit from shared skill or eval improvements.", ids, [], [f"skills/{skill}/SKILL.md"], "medium", 0.75)
        for skill, ids in by_skill.items()
        if len(ids) >= 2
    ]


def _shared_tags(projects: list[CrosslinkProjectRef]) -> list[CrosslinkPattern]:
    by_tag: dict[str, list[str]] = defaultdict(list)
    for project in projects:
        for tag in project.tags:
            by_tag[tag.lower()].append(project.project_id)
    patterns = []
    for tag, ids in by_tag.items():
        if len(ids) < 2:
            continue
        ptype = "shared_workflow" if tag in {"django", "viewflow", "workflow", "laboratory"} else "shared_project_convention"
        patterns.append(_pattern(ptype, f"Shared project tag: {tag}", f"Projects share `{tag}` metadata and may reuse guidance.", ids, [], ["ubongo/global/lessons-learned.md"], "medium" if tag in RISK_TERMS else "low", 0.65))
    return patterns


def _shared_risks(projects: list[CrosslinkProjectRef], evidence: list[CrosslinkEvidence]) -> list[CrosslinkPattern]:
    by_term: dict[str, set[str]] = defaultdict(set)
    for project in projects:
        text = " ".join(project.tags).lower()
        for term in RISK_TERMS:
            if term in text:
                by_term[term].add(project.project_id)
    for item in evidence:
        text = f"{item.summary or ''} {item.metadata}".lower()
        for term in RISK_TERMS:
            if term in text:
                by_term[term].add(item.project_id)
    return [
        _pattern("shared_risk", f"Shared risk theme: {term}", f"Risk term `{term}` appears across projects and should be reviewed as shared guidance.", sorted(ids), [item for item in evidence if item.project_id in ids], ["ubongo/global/engineering-standards.md", "evals/shared/risk-regression.yml"], "high" if term in {"auth", "authentication", "payment", "billing", "migration", "opensearch", "viewflow", "process"} else "medium", 0.7)
        for term, ids in by_term.items()
        if len(ids) >= 2
    ]


def _artifact_patterns(evidence: list[CrosslinkEvidence]) -> list[CrosslinkPattern]:
    by_need: dict[str, list[CrosslinkEvidence]] = defaultdict(list)
    for item in evidence:
        text = (item.summary or "").lower()
        if "missing test" in text or "regression" in text:
            by_need["shared_eval_need"].append(item)
        if "missing section" in text or "weak prompt" in text:
            by_need["shared_prompt_need"].append(item)
        if "secret" in text or "deploy" in text or "push directly" in text:
            by_need["shared_safety_rule"].append(item)
    patterns = []
    for ptype, items in by_need.items():
        projects = sorted({item.project_id for item in items})
        if len(projects) >= 2:
            target = "evals/shared/regression-case.yml" if ptype == "shared_eval_need" else "ubongo/global/engineering-standards.md"
            patterns.append(_pattern(ptype, ptype.replace("_", " ").title(), "Repeated artifact evidence suggests reusable guidance.", projects, items, [target], "high" if ptype == "shared_safety_rule" else "medium", 0.7))
    return patterns


def _pattern(ptype: str, title: str, summary: str, projects: list[str], evidence: list[CrosslinkEvidence], targets: list[str], risk: str, confidence: float) -> CrosslinkPattern:
    return CrosslinkPattern(pattern_id=f"pattern-{secrets.token_hex(3)}", pattern_type=ptype, title=title, summary=summary, projects=projects, evidence=evidence, suggested_targets=targets, risk_level=risk, confidence=confidence)
