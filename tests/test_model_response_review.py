from karakana.models.review.reviewer import review_response
from karakana.models.review.schemas import ResponseReview, ResponseReviewFinding


def test_response_review_schema_validation():
    review = ResponseReview(status="passed", findings=[ResponseReviewFinding("info", "low", "ok")])

    assert review.to_dict()["status"] == "passed"


def test_safe_response_passes_generic_review():
    review = review_response("This is a safe summary with tests and review notes.")

    assert review.status == "passed"
    assert not review.blocked


def test_dangerous_command_blocks():
    review = review_response("Run rm -rf . and delete all generated files.")

    assert review.blocked
    assert any(finding.finding_type == "destructive_command" for finding in review.findings)


def test_direct_push_to_main_blocks():
    review = review_response("Then git push origin main.")

    assert review.blocked
    assert any(finding.finding_type == "direct_main_push_instruction" for finding in review.findings)


def test_env_exposure_blocks():
    review = review_response("cat .env and show secrets.")

    assert review.blocked
    assert any(finding.finding_type == "env_file_modification" for finding in review.findings)


def test_production_deploy_blocks():
    review = review_response("Deploy to production immediately.")

    assert review.blocked
    assert any(finding.finding_type == "production_deploy_instruction" for finding in review.findings)


def test_missing_sections_warn_by_default_and_block_when_strict():
    warning_review = review_response("Safe text.", expected="plan", strict=False)
    strict_review = review_response("Safe text.", expected="plan", strict=True)

    assert warning_review.status == "warning"
    assert warning_review.warnings
    assert not warning_review.blocked
    assert strict_review.status == "blocked"
    assert strict_review.blocked
    assert any(finding.finding_type == "missing_required_sections" for finding in strict_review.findings)
