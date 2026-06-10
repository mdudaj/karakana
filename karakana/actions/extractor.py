"""Rule-based extraction of reviewable actions from model responses."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from karakana.actions.schemas import ActionBundle, ActionSource, ExtractedAction, StandardsSpecContext
from karakana.actions.store import generate_action_run_id
from karakana.skills.loader import SkillLoader
from karakana.traces.schemas import redact_value

ACTION_MARKERS = (
    "TODO:",
    "Next action:",
    "Next Actions",
    "Recommended action",
    "Create issue:",
    "Codex task:",
    "Update skill:",
    "Update ubongo:",
    "Add eval:",
    "Write tests:",
    "Documentation:",
    "Handoff:",
    "Suggested skills:",
    "Risk:",
    "Approval:",
    "Acceptance criteria:",
)
SECTION_HEADINGS = ("Next Actions", "TODOs", "Implementation Plan", "Tests", "Risks", "Proposed Changes", "Follow-up Tasks")
HIGH_RISK_TERMS = (
    "authentication",
    "permission",
    "billing",
    "payment",
    "migration",
    "database",
    "production",
    "deployment",
    "secret",
    "token",
    "workflow state",
    "viewflow process state",
    "opensearch index",
    "gepg callback",
    "oauth",
    "sso",
)

SKILL_KEYWORDS = {
    "viewflow-framework": ("viewflow", "workflow", "process state", "approval", "assignment", "transition"),
    "invenio-framework": ("invenio", "custom fields", "opensearch", "vocabulary", "oauth", "sso"),
    "gepg-billing": ("gepg", "billing", "payment callback", "payment", "reconciliation"),
    "django-debugging": ("django", "migration", "celery", "settings"),
    "github-pr-review": ("pr review", "acceptance criteria", "diff", "pull request"),
    "karakana-handoff": ("handoff", "next agent", "continue later"),
    "write-karakana-skill": ("new skill", "skill update", "skill metadata", "write skill"),
}


class ActionExtractor:
    def __init__(self, repo_root: Path | None = None):
        self.repo_root = repo_root

    def extract_from_response(
        self,
        response_path: Path,
        project: str | None = None,
        skill: str | None = None,
        require_passed_review: bool = False,
    ) -> ActionBundle:
        response = response_path.read_text(encoding="utf-8")
        review_status, review_blocked, review_path, warnings = self._review_state(response_path)
        run_id = _source_run_id(response_path)
        source = ActionSource("model_response", path=str(response_path), run_id=run_id, review_status=review_status, review_path=str(review_path) if review_path else None)
        action_run_id = generate_action_run_id()
        suggested_skills = self.extract_suggested_skills(response)
        standards_spec_context = extract_standards_spec_context(response)
        if review_blocked:
            action = ExtractedAction(
                action_id="action-001",
                action_type="manual_review",
                title="Review blocked model response",
                description="Source model response failed safety review. Inspect the review artifact before deciding any follow-up.",
                project=project,
                skill=skill,
                suggested_skills=suggested_skills,
                risk_level="high",
                evidence=[_excerpt(response)],
                tags=["blocked", "manual_review"],
                standards_spec_context=standards_spec_context,
            )
            return ActionBundle(
                action_run_id=action_run_id,
                status="blocked",
                created_at=now_utc(),
                source=source,
                summary="Source model response failed safety review; normal actions were not extracted.",
                suggested_skills=suggested_skills,
                standards_spec_context=standards_spec_context,
                actions=[action],
                warnings=["Source response review is blocked."],
                next_steps=["Inspect response-review.md before taking action."],
            )
        if require_passed_review and review_status not in {"passed", "warning"}:
            raise ValueError("A passed or warning response review is required before action extraction.")
        actions = self._extract_actions(response, project=project, skill=skill, suggested_skills=suggested_skills, standards_spec_context=standards_spec_context)
        if not actions:
            actions = [
                ExtractedAction(
                    action_id="action-001",
                    action_type="manual_review",
                    title="Manually review model response",
                    description=_first_sentence(response) or "Review the source response and decide next steps.",
                    project=project,
                    skill=skill,
                    suggested_skills=suggested_skills,
                    risk_level=_risk_level(response),
                    evidence=[_excerpt(response)],
                    tags=["fallback"],
                    standards_spec_context=standards_spec_context,
                )
            ]
        status = "ready_for_review" if actions else "draft"
        next_steps = ["Review generated action artifacts before publishing or handoff."]
        if review_status is None:
            warnings.append(f"No response review found. Run: karakana model review {response_path}")
        return ActionBundle(
            action_run_id=action_run_id,
            status=status,
            created_at=now_utc(),
            source=source,
            summary=f"Extracted {len(actions)} reviewable action(s) from model response.",
            suggested_skills=suggested_skills,
            standards_spec_context=standards_spec_context,
            actions=actions,
            warnings=warnings,
            next_steps=next_steps,
        )

    def _extract_actions(
        self,
        response: str,
        project: str | None,
        skill: str | None,
        suggested_skills: list[str],
        standards_spec_context: StandardsSpecContext | None,
    ) -> list[ExtractedAction]:
        candidates = _candidate_lines(response)
        actions: list[ExtractedAction] = []
        for index, text in enumerate(candidates, start=1):
            action_type = classify_action(text)
            cleaned = _clean_marker(text)
            if not cleaned:
                continue
            action = ExtractedAction(
                action_id=f"action-{index:03d}",
                action_type=action_type,
                title=_title(cleaned),
                description=cleaned,
                target_path=_target_path(cleaned, action_type),
                project=project,
                skill=skill,
                suggested_skills=self.extract_suggested_skills(cleaned) or suggested_skills,
                risk_level=_risk_level(cleaned),
                suggested_command=_suggested_command(action_type, cleaned),
                proposed_content=cleaned if action_type in {"memory_update", "skill_update", "prompt_update", "eval_case", "documentation_update", "improvement_proposal"} else None,
                evidence=[cleaned],
                tags=[action_type],
                standards_spec_context=standards_spec_context,
            )
            actions.append(action)
        return actions

    def extract_suggested_skills(self, text: str) -> list[str]:
        known = self._known_skill_names()
        found: set[str] = set()
        lowered = text.lower()
        for name in known:
            if name.lower() in lowered:
                found.add(name)
        for name, keywords in SKILL_KEYWORDS.items():
            if name in known and any(keyword in lowered for keyword in keywords):
                found.add(name)
        for skill in _suggested_skill_section_values(text):
            if skill in known:
                found.add(skill)
        return sorted(found)

    def _known_skill_names(self) -> set[str]:
        if not self.repo_root:
            root = Path.cwd()
        else:
            root = self.repo_root
        return set(SkillLoader(root / "skills").list_skills())

    @staticmethod
    def _review_state(response_path: Path) -> tuple[str | None, bool, Path | None, list[str]]:
        review_path = response_path.parent / "response-review.json"
        if not review_path.exists():
            return None, False, None, []
        data = json.loads(review_path.read_text(encoding="utf-8"))
        return data.get("status"), bool(data.get("blocked")), review_path, []


def classify_action(text: str) -> str:
    lowered = text.lower()
    if "create issue" in lowered:
        return "github_issue_draft"
    if "codex task" in lowered or "implement" in lowered:
        return "codex_task"
    if "update ubongo" in lowered:
        return "memory_update"
    if "update skill" in lowered:
        return "skill_update"
    if "add eval" in lowered or "regression case" in lowered:
        return "eval_case"
    if "documentation" in lowered or "readme" in lowered or "docs/" in lowered:
        return "documentation_update"
    if "manual review" in lowered or "approval" in lowered:
        return "manual_review"
    if "checklist" in lowered:
        return "implementation_checklist"
    if "handoff" in lowered or "next agent" in lowered:
        return "handoff"
    if "follow-up" in lowered or "next action" in lowered:
        return "follow_up_plan"
    return "implementation_checklist"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _candidate_lines(response: str) -> list[str]:
    lines = response.splitlines()
    candidates: list[str] = []
    capture = False
    for line in lines:
        stripped = line.strip()
        heading = re.match(r"^#+\s+(.+)$", stripped)
        if heading:
            capture = heading.group(1).strip() in SECTION_HEADINGS
            continue
        if any(stripped.lower().startswith(marker.lower()) for marker in ACTION_MARKERS):
            candidates.append(stripped)
        elif capture and re.match(r"^[-*]\s+", stripped):
            candidates.append(re.sub(r"^[-*]\s+", "", stripped))
    return candidates


def extract_standards_spec_context(response: str) -> StandardsSpecContext | None:
    standards = _section_text(response, "Standards Review")
    spec = _section_text(response, "Spec Review")
    acceptance = _section_lines(response, "Acceptance Criteria") + _section_lines(response, "Acceptance Criteria Check")
    standards_risks = _section_lines(standards or "", "Blocking Issues") + _section_lines(standards or "", "Non-blocking Suggestions")
    spec_gaps = _section_lines(spec or "", "Missing Requirements") + _section_lines(spec or "", "Over-Implementation")
    if not any([standards, spec, acceptance, standards_risks, spec_gaps]):
        return None
    return StandardsSpecContext(
        standards_summary=_first_sentence(standards or "") or (standards.strip() if standards else None),
        spec_summary=_first_sentence(spec or "") or (spec.strip() if spec else None),
        acceptance_criteria=acceptance,
        standards_risks=standards_risks,
        spec_gaps=spec_gaps,
    )


def _section_text(text: str, heading: str) -> str:
    pattern = rf"^##+\s+{re.escape(heading)}\s*$"
    lines = text.splitlines()
    capture = False
    captured: list[str] = []
    start_level = 0
    for line in lines:
        match = re.match(r"^(#+)\s+(.+?)\s*$", line.strip())
        if match and capture and len(match.group(1)) <= start_level:
            break
        if match and re.match(pattern, line.strip(), flags=re.IGNORECASE):
            capture = True
            start_level = len(match.group(1))
            continue
        if capture:
            captured.append(line)
    return "\n".join(captured).strip()


def _section_lines(text: str, heading: str) -> list[str]:
    section = _section_text(text, heading)
    if not section:
        return []
    values = []
    for line in section.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*]\s+", stripped):
            values.append(re.sub(r"^[-*]\s+", "", stripped))
    return values or [_first_sentence(section) or section.strip()]


def _suggested_skill_section_values(text: str) -> list[str]:
    values = []
    section = _section_text(text, "Suggested Skills")
    if section:
        for line in section.splitlines():
            stripped = re.sub(r"^[-*]\s+", "", line.strip())
            values.extend(part.strip(" `.,") for part in re.split(r",|;", stripped) if part.strip())
    for line in text.splitlines():
        if line.strip().lower().startswith("suggested skills:"):
            value = line.split(":", 1)[1]
            values.extend(part.strip(" `.,") for part in re.split(r",|;", value) if part.strip())
    return values


def _clean_marker(text: str) -> str:
    text = re.sub(r"^[-*]\s+", "", text.strip())
    for marker in ACTION_MARKERS:
        if text.lower().startswith(marker.lower()):
            return text[len(marker) :].strip()
    return text


def _risk_level(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in HIGH_RISK_TERMS):
        return "high"
    return "low"


def _title(text: str) -> str:
    text = " ".join(text.split())
    return text[:80].rstrip(".") or "Review action"


def _target_path(text: str, action_type: str) -> str | None:
    match = re.search(r"`([^`]+)`", text)
    if match:
        return match.group(1)
    if action_type == "eval_case":
        return "evals/"
    if action_type == "memory_update":
        return "ubongo/"
    if action_type == "skill_update":
        return "skills/"
    if action_type == "documentation_update":
        return "docs/"
    return None


def _suggested_command(action_type: str, text: str) -> str | None:
    if action_type == "codex_task":
        return "karakana codex run --project <project> --skill <skill> --task '<task>'"
    if action_type == "github_issue_draft":
        return "karakana action publish <action-run-id> --create-issues"
    return None


def _first_sentence(text: str) -> str:
    match = re.search(r"(.+?[.!?])(\s|$)", " ".join(text.split()))
    return match.group(1) if match else ""


def _excerpt(text: str, limit: int = 500) -> str:
    text = redact_value(" ".join(text.split()))
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _source_run_id(path: Path) -> str | None:
    parts = path.parts
    if "runs" in parts:
        index = parts.index("runs")
        if len(parts) > index + 1:
            return parts[index + 1]
    return None
