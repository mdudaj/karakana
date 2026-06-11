from karakana.requirements.schemas import HarnessSubsystemImpact, RequirementPRD, RequirementSource


def test_requirements_schema_round_trip():
    prd = RequirementPRD(
        req_id="req",
        title="Title",
        project="karakana",
        skillpack="karakana",
        status="ready_for_review",
        source=RequirementSource(source_type="note", title="Note"),
        context="Context",
        problem="Problem",
        goal="Goal",
        harness_impact=HarnessSubsystemImpact(instructions=["Do"], tools=["karakana"], environment=["local"], state=["trace"], feedback=["tests"]),
    )

    loaded = RequirementPRD.from_dict(prd.to_dict())

    assert loaded.source.source_type == "note"
    assert loaded.harness_impact.instructions == ["Do"]
