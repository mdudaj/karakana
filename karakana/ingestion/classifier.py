"""Rule-based ingestion classification."""

from __future__ import annotations

from karakana.ingestion.schemas import ClassificationResult

RULES = {
    "safety_update": ["secret exposure", "destructive command", "production deployment", "direct push to main", "bypass review", "bypass tests", "permission change", "authentication risk", ".env"],
    "eval_update": ["regression", "repeated failure", "missed issue", "safety violation", "expected output", "acceptance criteria", "test gap", "missing test"],
    "skill_update": ["repeated workflow", "checklist", "debugging procedure", "pitfall", "verification step", "when to use", "when not to use", "safety rule", "approval requirement"],
    "prompt_update": ["output format problem", "missing section", "bad instruction", "weak prompt", "wrong model route", "incomplete artifact"],
    "behavior_update": ["correction from user", "preferred style", "format preference", "approval preference", "response style", "copy-ready markdown"],
    "project_convention": ["standard command", "standard workflow", "coding convention", "branch convention", "review convention", "approval convention"],
    "ubongo_memory": ["architecture decision", "deployment note", "known issue", "project convention", "command", "dependency detail", "configuration rule", "troubleshooting note"],
}


def classify_content(text: str, project: str | None = None, skillpack_context=None) -> ClassificationResult:
    lowered = text.lower()
    scores = {category: sum(1 for indicator in indicators if indicator in lowered) for category, indicators in RULES.items()}
    category, score = max(scores.items(), key=lambda item: item[1])
    if score == 0:
        category = "manual_review"
    risk = "high" if category == "safety_update" or any(word in lowered for word in ["authentication", "payment", "migration", "opensearch", "viewflow", "production"]) else "low"
    targets = suggested_targets(category, project, skillpack_context)
    return ClassificationResult(
        category=category,
        confidence=min(1.0, 0.35 + (score * 0.2)) if category != "manual_review" else 0.2,
        rationale=f"Matched {score} rule indicator(s) for {category}." if category != "manual_review" else "No strong rule match; manual review required.",
        suggested_targets=targets,
        risk_level=risk,
    )


def suggested_targets(category: str, project: str | None, skillpack_context=None) -> list[str]:
    project_key = project or (skillpack_context.skillpack.project.id if skillpack_context else "project")
    if category == "ubongo_memory":
        return [f"ubongo/projects/{project_key}/known-issues.md", f"ubongo/projects/{project_key}/workflows.md"]
    if category == "skill_update":
        skills = skillpack_context.required_skills if skillpack_context else []
        return [f"skills/{skills[0]}/SKILL.md"] if skills else ["skills/<skill>/SKILL.md"]
    if category == "eval_update":
        return [f"evals/{project_key}/regression-case.yml"]
    if category == "prompt_update":
        return ["prompts/planner.prompt.md"]
    if category == "safety_update":
        return ["docs/safety-notes.md"]
    if category == "behavior_update":
        return ["ubongo/global/lessons-learned.md"]
    if category == "project_convention":
        return [f"ubongo/projects/{project_key}/workflows.md"]
    return []
