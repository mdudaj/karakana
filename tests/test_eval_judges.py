from karakana.evals.judges import check_forbidden_patterns, check_required_sections, judge_output
from karakana.evals.schemas import EvalCase, EvalExpectation, EvalInput


def case(expectations: EvalExpectation) -> EvalCase:
    return EvalCase(
        id="case",
        name="Case",
        description="",
        suite="safety",
        input=EvalInput(task="Task"),
        expectations=expectations,
    )


def test_judge_checks_text_sections_patterns_and_route():
    output = "# Plan\n\n## Risks\n\nNo secret values here.\n"
    result = judge_output(
        output,
        case(
            EvalExpectation(
                must_include=["secret"],
                must_not_include=["deploy directly"],
                required_sections=["Risks"],
                forbidden_patterns=["GITHUB_TOKEN"],
                expected_provider="github",
                expected_model="gpt-5-mini",
            )
        ),
        {"provider": "github", "model": "gpt-5-mini"},
    )

    assert result.status == "passed"
    assert result.score == 1.0


def test_judge_fails_blocking_checks():
    result = judge_output("unsafe deploy directly", case(EvalExpectation(must_include=["missing"], must_not_include=["deploy directly"])), {})

    assert result.status == "failed"
    assert result.score == 0.0
    assert result.failed_checks


def test_section_and_forbidden_helpers():
    assert check_required_sections("## Tests\n", ["Tests"]) == []
    assert check_required_sections("No heading\n", ["Tests"]) == ["Tests"]
    assert check_forbidden_patterns("GITHUB_TOKEN=abc", ["GITHUB_TOKEN"]) == ["GITHUB_TOKEN"]
