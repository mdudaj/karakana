from karakana.crosslinks.classifier import classify_pattern
from karakana.crosslinks.schemas import CrosslinkPattern


def test_classifies_shared_risk_as_global_ubongo_update():
    pattern = CrosslinkPattern(
        pattern_id="pattern-1",
        pattern_type="shared_risk",
        title="Shared payment risk",
        summary="Payment risk appears in multiple projects.",
        projects=["billing", "nhrdm"],
        risk_level="high",
    )

    proposal = classify_pattern(pattern)

    assert proposal["proposal_type"] == "global_ubongo_update"
    assert proposal["target"] == "ubongo/global/engineering-standards.md"


def test_classifies_conflict_as_manual_review():
    pattern = CrosslinkPattern(
        pattern_id="pattern-1",
        pattern_type="conflicting_memory",
        title="Conflicting convention",
        summary="Projects disagree.",
        projects=["billing", "lims"],
        risk_level="medium",
    )

    proposal = classify_pattern(pattern)

    assert proposal["proposal_type"] == "manual_review"
    assert proposal["target"] is None
