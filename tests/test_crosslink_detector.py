from karakana.crosslinks.detector import detect_patterns
from karakana.crosslinks.schemas import CrosslinkEvidence, CrosslinkProjectRef


def test_detects_shared_workflow_and_risk_patterns():
    projects = [
        CrosslinkProjectRef(project_id="billing", tags=["django", "workflow"]),
        CrosslinkProjectRef(project_id="lims", tags=["django", "workflow"]),
    ]

    patterns = detect_patterns(projects, [])
    types = {pattern.pattern_type for pattern in patterns}

    assert "shared_workflow" in types
    assert "shared_risk" in types


def test_detects_shared_eval_prompt_and_safety_needs():
    evidence = [
        CrosslinkEvidence(project_id="billing", source_type="patch_review", summary="missing test for regression"),
        CrosslinkEvidence(project_id="lims", source_type="patch_review", summary="missing test for regression"),
        CrosslinkEvidence(project_id="nhrdm", source_type="trace", summary="missing section in prompt"),
        CrosslinkEvidence(project_id="karakana", source_type="trace", summary="missing section in prompt"),
        CrosslinkEvidence(project_id="billing", source_type="patch_review", summary="secret deploy warning"),
        CrosslinkEvidence(project_id="lims", source_type="patch_review", summary="secret deploy warning"),
    ]

    patterns = detect_patterns([], evidence)
    types = {pattern.pattern_type for pattern in patterns}

    assert "shared_eval_need" in types
    assert "shared_prompt_need" in types
    assert "shared_safety_rule" in types
