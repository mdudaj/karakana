"""First-encounter task context. Completeness never grants readiness or authority."""

from __future__ import annotations

import re

BRIEF_FIELDS = {
    "project_purpose": "Project and purpose",
    "related_feature": "Related feature/capability",
    "beneficiary": "People/workflow affected",
    "task_relevance": "Problem and relevance now",
    "current_state": "Current state and prerequisites",
    "intended_outcome": "Intended outcome",
    "scope_and_authority": "Scope and authority",
    "references": "Governing evidence",
}
_PLACEHOLDER = re.compile(
    r"(?:todo|tbd|unknown|unconfirmed|not recorded|not supplied|not provided|n/?a)"
    r"(?:\s*[:\-–—].*)?", re.IGNORECASE,
)


def render_brief_guidance() -> str:
    """Conditional guidance shared by planning, document and execution prompts."""
    return """When creating a task brief or next-task brief, begin with first-encounter context
before technical steps: project/product purpose; related feature/capability in plain
language (ID plus name where available); people/workflow affected; the problem,
task relevance and why now; current state/prerequisites; intended outcome;
scope and authority; and governing evidence. Show product → feature → this task.
Explain local acronyms. Make current versus intended state and accepted versus
proposed scope explicit. State the immediate contribution without claiming that
downstream features are delivered. Keep the introduction compact and self-contained;
links supplement it. Retain existing acceptance, steps, risks and verification.
Source facts from current project evidence; mark missing context unconfirmed and
name how to resolve it. Do not infer purpose, users or approval from an identifier.
Check whether a new developer can explain what is worked on and why without
opening links or reading chat history. Structure alone cannot establish relevance,
truth, readiness or acceptance. This convention preserves the requested action;
an inquiry/review is not converted into a task or implementation authorization."""


def redact_brief_context(value):
    """Use existing handoff redaction for optional context in JSON and Markdown."""
    if isinstance(value, str):
        # Handoff's package entrypoint imports lifecycle guidance. Defer this
        # dependency so importing shared guidance does not import its consumer.
        from karakana.handoffs.redaction import redact_handoff_text
        return redact_handoff_text(value)
    if isinstance(value, dict):
        return {key: redact_brief_context(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_brief_context(item) for item in value]
    return value


def _known(value) -> bool:
    return (isinstance(value, str) and bool(value.strip())
            and not _PLACEHOLDER.fullmatch(value.strip())
            and not (value.strip().startswith("[") and value.strip().endswith("]")))


def assess_brief_context(value) -> dict:
    """Check authored field coverage only; never load references or infer facts."""
    data = value if isinstance(value, dict) else {}
    missing = []
    for key in BRIEF_FIELDS:
        item = data.get(key)
        valid = (isinstance(item, list) and bool(item) and all(_known(x) for x in item)
                 if key == "references" else _known(item))
        if not valid:
            missing.append(key)
    unexpected = sorted(str(key) for key in data if key not in BRIEF_FIELDS)
    return {"status": "needs_context" if missing or unexpected else "complete",
            "missing": missing, "unexpected": unexpected}


def render_brief_context(value) -> str:
    """Render explicit gaps in legacy/partial tasks before technical detail."""
    data = redact_brief_context(value) if isinstance(value, dict) else {}
    assessment = assess_brief_context(data)
    lines = ["## Task Context", ""]
    for key, label in BRIEF_FIELDS.items():
        item = data.get(key)
        if key in assessment["missing"]:
            text = "Unconfirmed — resolve from current project evidence."
            if isinstance(item, str) and re.match(r"(?i)^(?:unconfirmed|unknown)\s*[:\-–—]\s*\S", item.strip()):
                text = item.strip()  # Retain an authored owner/resolution step.
            elif key == "references" and isinstance(item, list) and any(_known(x) for x in item):
                text = "; ".join(x if _known(x) else "Unconfirmed reference" for x in item)
        else:
            text = "; ".join(item) if key == "references" else item
        text = " ".join(text.splitlines())
        lines.append(f"- **{label}:** {text}")
    lines.extend(["", f"Context completeness: `{assessment['status']}`.",
                  "Field coverage only; facts, relevance, readiness and authority still require review."])
    if assessment["unexpected"]:
        # Do not echo arbitrary keys or values into the prompt.
        lines.append("Unexpected context fields supplied; reconcile the documented contract.")
    return "\n".join(lines)
