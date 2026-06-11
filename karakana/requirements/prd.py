"""Deterministic PRD generation."""

from __future__ import annotations

from karakana.models.router import route_model
from karakana.requirements.schemas import HarnessSubsystemImpact, RequirementPRD, RequirementSource, StandardsSpecContext
from karakana.requirements.store import generate_req_id


def generate_prd(
    source: RequirementSource,
    content: str,
    *,
    project: str | None = None,
    skillpack_context=None,
) -> RequirementPRD:
    project_key = project or source.project or (skillpack_context.skillpack.project.id if skillpack_context else None)
    skillpack_name = source.skillpack or (skillpack_context.skillpack.name if skillpack_context else None)
    route = route_model("planning", skillpack_routes=skillpack_context.model_routes if skillpack_context else None)
    title = _title(source, content)
    standards_spec = _standards_spec(content)
    non_goals = standards_spec.non_goals or ["Do not execute Codex automatically.", "Do not publish issues or pull requests by default.", "Do not mutate repository files from requirements artifacts."]
    skills = _skills(content, skillpack_context)
    safety = _safety(content, skillpack_context)
    tests = _tests(content, skillpack_context)
    return RequirementPRD(
        req_id=generate_req_id(),
        title=title,
        project=project_key,
        skillpack=skillpack_name,
        status="ready_for_review",
        source=source,
        context=_excerpt(content),
        problem=_problem(content),
        goal=_goal(content),
        non_goals=non_goals,
        users_or_actors=["developer", "reviewer", "Karakana operator"],
        functional_requirements=_functional_requirements(content),
        non_functional_requirements=["Requirements must be deterministic and reviewable.", "Artifacts must stay under .karakana/requirements/.", "Live models, Codex execution, publishing, and deployment remain opt-in or out of scope."],
        harness_impact=_harness_impact(content, skillpack_context),
        standards_spec=standards_spec,
        risks=_risks(content),
        safety_constraints=safety,
        suggested_skills=skills,
        suggested_skillpack=skillpack_name,
        model_route=route,
        test_and_eval_plan=tests,
        rollout_or_review_plan=["Generate PRD artifact.", "Review stories and issue drafts.", "Run readiness checks.", "Hand off only after human review."],
        metadata={"inferred": True, "source_type": source.source_type},
    )


def _title(source: RequirementSource, content: str) -> str:
    if source.title and source.title != "Manual note":
        return f"Requirements for {source.title}"
    first = next((line.strip("# -") for line in content.splitlines() if line.strip()), "Requirement")
    return first[:90]


def _problem(content: str) -> str:
    if "problem" in content.lower():
        return "Source includes problem context; review extracted context for exact scope."
    return "Needs review: source describes intent, but problem statement should be confirmed."


def _goal(content: str) -> str:
    first = next((line.strip(" -#") for line in content.splitlines() if line.strip()), "Produce structured requirements before implementation.")
    return f"Convert the source intent into reviewable requirements: {first[:180]}"


def _functional_requirements(content: str) -> list[str]:
    lowered = content.lower()
    requirements = ["Generate a PRD with context, problem, goal, requirements, risks, safety constraints, and review plan.", "Generate user stories and issue drafts as separate reviewable artifacts.", "Run Definition of Ready checks before handoff."]
    if "codex" in lowered:
        requirements.append("Preserve Codex handoff boundaries and do not execute Codex.")
    if "issue" in lowered:
        requirements.append("Create issue drafts only; do not publish GitHub issues by default.")
    if "ingest" in lowered or "memory" in lowered:
        requirements.append("Preserve ingestion evidence and avoid direct memory or skill writes.")
    return requirements


def _harness_impact(content: str, skillpack_context=None) -> HarnessSubsystemImpact:
    return HarnessSubsystemImpact(
        instructions=["Clarify developer intent before implementation.", "Preserve Standards-vs-Spec context.", "Keep generated tasks reviewable."],
        tools=["karakana requirements", "karakana eval run --suite requirements", "pytest"],
        environment=["Local repository only.", "No live model calls required.", "No GitHub publishing by default."],
        state=["Source artifact metadata.", "Skillpack context when available.", "Requirement, story, issue, and readiness artifacts."],
        feedback=["Definition of Ready review.", "Requirements eval suite.", "Human review before Codex handoff or publishing."] + (skillpack_context.test_commands if skillpack_context else []),
    )


def _standards_spec(content: str) -> StandardsSpecContext:
    lowered = content.lower()
    standards = ["Engineering changes must be reviewable, tested, and safety-gated.", "No secrets, deployments, pushes, PRs, or live model calls by default."]
    spec = ["Needs review: confirm exact user-facing behavior and scope."]
    acceptance = ["PRD includes all required sections.", "Stories include acceptance criteria.", "Issues are independently grabbable vertical slices.", "Readiness check reports missing information."]
    if "standards review" in lowered:
        standards.append("Source included Standards Review context; preserve it during decomposition.")
    if "spec review" in lowered:
        spec.append("Source included Spec Review context; preserve acceptance criteria and scope gaps.")
    return StandardsSpecContext(standards=standards, spec=spec, acceptance_criteria=acceptance, non_goals=[])


def _skills(content: str, skillpack_context=None) -> list[str]:
    skills = list(skillpack_context.required_skills) if skillpack_context else []
    lowered = content.lower()
    mapping = {
        "viewflow-framework": ["viewflow", "workflow", "process state"],
        "invenio-framework": ["invenio", "opensearch", "custom field"],
        "gepg-billing": ["gepg", "billing", "payment"],
        "github-pr-review": ["pr review", "acceptance criteria"],
        "karakana-handoff": ["handoff", "next agent"],
    }
    for skill, terms in mapping.items():
        if any(term in lowered for term in terms) and skill not in skills:
            skills.append(skill)
    return skills or ["karakana-self-improvement"]


def _safety(content: str, skillpack_context=None) -> list[str]:
    safety = ["Do not execute Codex.", "Do not call live models by default.", "Do not publish GitHub issues by default.", "Do not push, deploy, or create PRs."]
    if skillpack_context:
        safety.extend([f"Approval required: {item}" for item in skillpack_context.skillpack.safety.requires_approval_for])
    if any(term in content.lower() for term in ["auth", "payment", "migration", "secret", "production", "process state"]):
        safety.append("High-risk domain terms require explicit review and model escalation.")
    return safety


def _tests(content: str, skillpack_context=None) -> list[str]:
    tests = ["karakana eval run --suite requirements", "pytest"]
    if skillpack_context:
        tests.extend(skillpack_context.test_commands)
    if "ingest" in content.lower():
        tests.append("karakana eval run --suite ingestion")
    return list(dict.fromkeys(tests))


def _risks(content: str) -> list[str]:
    risks = ["Vague source material can produce vague stories without human review."]
    if any(term in content.lower() for term in ["auth", "payment", "migration", "production", "secret", "workflow"]):
        risks.append("High-risk project behavior may require stronger review before implementation.")
    return risks


def _excerpt(content: str, limit: int = 1200) -> str:
    text = content.strip()
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."
