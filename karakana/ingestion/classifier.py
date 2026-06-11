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

MSC_PLATFORM_RULES = {
    "research_objective_mapping": ["objective-to-feature-to-evidence", "research objective", "evidence produced", "platform capability"],
    "curriculum_source_registry": ["source registry", "tier 1", "tanzania institute of education", "official_url"],
    "curriculum_snapshot": ["snapshot manifest", "fetch manifest", "checksums.sha256", "downloaded_sources"],
    "deterministic_extraction": ["deterministic extraction", "normalized curriculum", "raw extracted text", "extractor version"],
    "topic_screening": ["topic screening", "animation suitability", "deprioritized", "candidate topic"],
    "automated_curriculum_review": ["automated curriculum review", "verbalized", "judgment distribution", "uncertainty flags"],
    "human_topic_selection_gate": ["human topic selection", "topic_selection_decisions", "human acceptance", "accepted shortlist"],
    "evaluation_workflow": ["evaluation workflow", "expert review", "rubric scoring", "review submission"],
    "evidence_artifact": ["evidence model", "evidence artifact", "generation manifest", "rubric response"],
    "rubric": ["rubric", "curriculum alignment", "scientific accuracy", "production practicality"],
    "export_plan": ["export plan", "csv", "json", "zip bundle", "analysis tables"],
    "provenance_replay": ["provenance", "replay", "reconstruction", "divergence"],
    "whatsapp_evaluator_channel": ["whatsapp", "secondary evaluator", "opt-in", "secure review link"],
    "configurable_workflow_engine": ["configurable workflow", "researchworkflow", "viewflow", "execution manifest"],
    "commit_push_safety": ["commit/push", "no push", "force push", "remote verification"],
    "vertical_implementation_slice": ["slice 1", "vertical slice", "acceptance criteria", "verification command"],
}


def classify_content(text: str, project: str | None = None, skillpack_context=None) -> ClassificationResult:
    lowered = text.lower()
    if project == "msc-platform":
        msc_scores = {category: sum(1 for indicator in indicators if indicator in lowered) for category, indicators in MSC_PLATFORM_RULES.items()}
        msc_category, msc_score = max(msc_scores.items(), key=lambda item: item[1])
        if msc_score > 0:
            risk = "high" if msc_category in {"automated_curriculum_review", "whatsapp_evaluator_channel", "commit_push_safety"} else "low"
            return ClassificationResult(
                category=msc_category,
                confidence=min(1.0, 0.45 + (msc_score * 0.15)),
                rationale=f"Matched {msc_score} msc-platform indicator(s) for {msc_category}.",
                suggested_targets=suggested_targets(msc_category, project, skillpack_context),
                risk_level=risk,
            )

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
    if project_key == "msc-platform":
        msc_targets = {
            "research_objective_mapping": ["ubongo/projects/msc-platform/overview.md", "ubongo/projects/msc-platform/evaluation-workflows.md"],
            "curriculum_source_registry": ["ubongo/projects/msc-platform/curriculum-data.md"],
            "curriculum_snapshot": ["ubongo/projects/msc-platform/curriculum-data.md", "evals/msc-platform/curriculum-snapshot.yml"],
            "deterministic_extraction": ["ubongo/projects/msc-platform/curriculum-data.md"],
            "topic_screening": ["ubongo/projects/msc-platform/curriculum-data.md"],
            "automated_curriculum_review": ["ubongo/projects/msc-platform/curriculum-data.md", "skills/research-platform/SKILL.md"],
            "human_topic_selection_gate": ["ubongo/projects/msc-platform/evaluation-workflows.md"],
            "evaluation_workflow": ["ubongo/projects/msc-platform/evaluation-workflows.md"],
            "evidence_artifact": ["ubongo/projects/msc-platform/evidence-model.md"],
            "rubric": ["ubongo/projects/msc-platform/evaluation-workflows.md"],
            "export_plan": ["ubongo/projects/msc-platform/evidence-model.md"],
            "provenance_replay": ["ubongo/projects/msc-platform/evidence-model.md"],
            "whatsapp_evaluator_channel": ["ubongo/projects/msc-platform/evaluation-workflows.md", "skills/research-platform/SKILL.md"],
            "configurable_workflow_engine": ["ubongo/projects/msc-platform/architecture.md", "skills/research-platform/SKILL.md"],
            "commit_push_safety": ["ubongo/projects/msc-platform/architecture.md"],
            "vertical_implementation_slice": ["ubongo/projects/msc-platform/implementation-slices.md", "evals/msc-platform/vertical-slices.yml"],
        }
        if category in msc_targets:
            return msc_targets[category]
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
