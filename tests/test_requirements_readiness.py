from karakana.requirements.prd import generate_prd
from karakana.requirements.readiness import check_readiness
from karakana.requirements.schemas import RequirementSource


def test_readiness_checks_report_ready():
    prd = generate_prd(RequirementSource(source_type="note"), "Add readiness checks for safety constraints and model route.")

    check = check_readiness(prd)

    assert check.ready
    assert "model route is recommended" in check.passed
    assert not check.failed
