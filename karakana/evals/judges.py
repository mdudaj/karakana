"""Rule-based evaluation judges."""

from __future__ import annotations

import re

from karakana.evals.schemas import EvalCase, EvalCaseResult


def judge_output(output: str, case: EvalCase, metadata: dict) -> EvalCaseResult:
    passed: list[str] = []
    failed: list[str] = []
    warnings: list[str] = []
    expectations = case.expectations
    lowered = output.lower()

    for value in expectations.must_include:
        if value.lower() in lowered:
            passed.append(f"must_include: {value}")
        else:
            failed.append(f"missing required text: {value}")

    for value in expectations.must_not_include:
        if value.lower() in lowered:
            failed.append(f"forbidden text present: {value}")
        else:
            passed.append(f"must_not_include: {value}")

    missing_sections = check_required_sections(output, expectations.required_sections)
    for section in expectations.required_sections:
        if section in missing_sections:
            failed.append(f"missing required section: {section}")
        else:
            passed.append(f"required_section: {section}")

    forbidden = check_forbidden_patterns(output, expectations.forbidden_patterns)
    for pattern in expectations.forbidden_patterns:
        if pattern in forbidden:
            failed.append(f"forbidden pattern present: {pattern}")
        else:
            passed.append(f"forbidden_pattern_absent: {pattern}")

    if expectations.max_length is not None:
        if len(output) <= expectations.max_length:
            passed.append(f"max_length: {expectations.max_length}")
        else:
            failed.append(f"output exceeds max_length: {expectations.max_length}")
    if expectations.min_length is not None:
        if len(output) >= expectations.min_length:
            passed.append(f"min_length: {expectations.min_length}")
        else:
            failed.append(f"output below min_length: {expectations.min_length}")

    if expectations.expected_provider:
        actual_provider = metadata.get("provider")
        if actual_provider == expectations.expected_provider:
            passed.append(f"expected_provider: {actual_provider}")
        else:
            failed.append(f"expected provider {expectations.expected_provider}, got {actual_provider}")
    if expectations.expected_model:
        actual_model = metadata.get("model")
        if actual_model == expectations.expected_model:
            passed.append(f"expected_model: {actual_model}")
        else:
            failed.append(f"expected model {expectations.expected_model}, got {actual_model}")

    safety_checks = set(metadata.get("safety_flags") or [])
    for flag in expectations.safety_flags:
        if flag in safety_checks or flag.lower() in lowered:
            passed.append(f"safety_flag: {flag}")
        else:
            warnings.append(f"safety flag not observed: {flag}")

    status = "failed" if failed else ("warning" if warnings else "passed")
    score = 0.0 if failed else (0.5 if warnings else 1.0)
    return EvalCaseResult(
        case_id=case.id,
        status=status,
        score=score,
        passed_checks=passed,
        failed_checks=failed,
        warnings=warnings,
        output_excerpt=_excerpt(output),
    )


def check_required_sections(output: str, sections: list[str]) -> list[str]:
    missing: list[str] = []
    for section in sections:
        pattern = rf"^\s*#+\s+{re.escape(section)}\s*$"
        if not re.search(pattern, output, flags=re.IGNORECASE | re.MULTILINE):
            missing.append(section)
    return missing


def check_forbidden_patterns(output: str, patterns: list[str]) -> list[str]:
    found: list[str] = []
    for pattern in patterns:
        if re.search(pattern, output, flags=re.IGNORECASE):
            found.append(pattern)
    return found


def _excerpt(output: str, limit: int = 800) -> str:
    text = output.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."
