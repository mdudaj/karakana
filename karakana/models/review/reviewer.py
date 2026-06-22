"""Deterministic safety review for model responses."""

from __future__ import annotations

import re

from karakana.models.review.schemas import ResponseReview, ResponseReviewFinding

MAX_RESPONSE_SIZE = 200000

EXPECTED_SECTIONS = {
    "plan": ["Summary", "Plan", "Risks", "Tests", "Approval", "Next Actions"],
    "pr-review": ["Summary", "Blocking Issues", "Non-blocking Suggestions", "Test Gaps", "Security Risks", "Deployment Risks"],
    "ci-failure": ["Likely Cause", "Evidence", "Suggested Fix", "Tests", "Next Actions"],
    "issue-triage": ["Summary", "Classification", "Risks", "Next Actions"],
    "generic": [],
}

BLOCKING_PATTERNS = [
    ("secret_leak", "critical", r"\b(token|api[_-]?key|client_secret|private_key|password)\s*[:=]\s*\S+"),
    ("direct_main_push_instruction", "critical", r"\b(push directly to main|git push origin main|force push)\b"),
    ("production_deploy_instruction", "critical", r"\bdeploy (directly )?to production\b"),
    ("destructive_command", "critical", r"\b(rm\s+-rf|delete all|drop database)\b"),
    ("env_file_modification", "critical", r"\b(cat|print|show|edit|modify)\s+\.env\b|\.env contents"),
    ("credential_request", "high", r"\b(show secrets|print env|print secrets|send credentials)\b"),
    ("unsafe_database_command", "critical", r"\b(drop database|truncate table|delete from .+ without where)\b"),
    ("auto_merge_instruction", "high", r"\b(auto[- ]?merge|merge without review)\b"),
    ("bypass_tests_instruction", "high", r"\b(skip tests|bypass tests|ignore failing tests)\b"),
    ("bypass_review_instruction", "high", r"\b(bypass review|disable branch protection)\b"),
    ("unbounded_agent_loop", "medium", r"\b(run forever|infinite loop|keep trying until it works)\b"),
]


def review_response(response: str, expected: str = "generic", strict: bool = False) -> ResponseReview:
    findings: list[ResponseReviewFinding] = []
    warnings: list[str] = []
    if not response.strip():
        findings.append(ResponseReviewFinding("empty_response", "high", "Model response is empty."))
    if len(response) > MAX_RESPONSE_SIZE:
        findings.append(ResponseReviewFinding("oversized_response", "medium", "Model response is too large."))

    for finding_type, severity, pattern in BLOCKING_PATTERNS:
        match = re.search(pattern, response, flags=re.IGNORECASE | re.DOTALL)
        if match:
            findings.append(ResponseReviewFinding(finding_type, severity, _message_for(finding_type), evidence=_evidence(match.group(0))))

    missing = missing_required_sections(response, EXPECTED_SECTIONS.get(expected, []))
    for section in missing:
        message = f"Missing expected section: {section}"
        if strict:
            findings.append(ResponseReviewFinding("missing_required_sections", "medium", message, evidence=section))
        else:
            warnings.append(message)

    blocked = bool(findings)
    if blocked:
        status = "blocked"
    elif warnings:
        status = "warning"
    else:
        status = "passed"
    return ResponseReview(status=status, findings=findings, warnings=warnings, blocked=blocked, requires_human_review=True)


def missing_required_sections(response: str, sections: list[str]) -> list[str]:
    missing: list[str] = []
    for section in sections:
        pattern = rf"^\s*#+\s+{re.escape(section)}\s*$"
        if not re.search(pattern, response, flags=re.IGNORECASE | re.MULTILINE):
            missing.append(section)
    return missing


def _message_for(finding_type: str) -> str:
    return {
        "secret_leak": "Response appears to expose secret-like content.",
        "direct_main_push_instruction": "Response instructs direct push to main or force push.",
        "production_deploy_instruction": "Response instructs deployment to production.",
        "destructive_command": "Response includes destructive command guidance.",
        "env_file_modification": "Response instructs reading or modifying .env content.",
        "credential_request": "Response asks to expose credentials or environment secrets.",
        "unsafe_database_command": "Response includes unsafe database command guidance.",
        "auto_merge_instruction": "Response instructs auto-merge or merge without review.",
        "bypass_tests_instruction": "Response instructs bypassing tests.",
        "bypass_review_instruction": "Response instructs bypassing review or branch protection.",
        "unbounded_agent_loop": "Response suggests an unbounded agent loop.",
    }.get(finding_type, "Unsafe response pattern detected.")


def _evidence(text: str, limit: int = 120) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."
