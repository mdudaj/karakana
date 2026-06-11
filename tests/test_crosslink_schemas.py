import pytest

from karakana.crosslinks.schemas import CrosslinkBundle, CrosslinkEvidence, CrosslinkPattern, CrosslinkProjectRef, CrosslinkProposal


def test_crosslink_schema_serialization_redacts_secrets():
    evidence = CrosslinkEvidence(project_id="billing", source_type="trace", summary="api_key=abc123 repeated issue")
    pattern = CrosslinkPattern(
        pattern_id="pattern-1",
        pattern_type="shared_safety_rule",
        title="Shared safety",
        summary="Repeated secret handling issue",
        projects=["billing", "lims"],
        evidence=[evidence],
        risk_level="high",
    )
    proposal = CrosslinkProposal(
        proposal_id="proposal-1",
        proposal_type="global_ubongo_update",
        title="Update safety memory",
        summary="Add shared safety note",
        target_path="ubongo/global/engineering-standards.md",
        proposed_content="Do not print OPENAI_API_KEY.",
        affected_projects=["billing", "lims"],
    )
    bundle = CrosslinkBundle(
        crosslink_id="crosslink-1",
        workspace="nimr",
        status="ready_for_review",
        created_at="2026-06-10T00:00:00Z",
        projects=[CrosslinkProjectRef(project_id="billing")],
        patterns=[pattern],
        proposals=[proposal],
    )

    data = bundle.to_dict()

    assert data["patterns"][0]["pattern_type"] == "shared_safety_rule"
    assert "OPENAI_API_KEY" not in str(data)


def test_crosslink_schema_rejects_invalid_values():
    with pytest.raises(ValueError):
        CrosslinkPattern(pattern_id="p", pattern_type="unknown", title="Bad", summary="Bad")

    with pytest.raises(ValueError):
        CrosslinkProposal(proposal_id="p", proposal_type="unknown", title="Bad", summary="Bad")

