import pytest

from karakana.dogfood.schemas import DogfoodBacklogItem, DogfoodCommandResult, DogfoodFinding, DogfoodRun
from karakana.dogfood.summary import generate_dogfood_id


def test_dogfood_schema_serialization_and_id():
    run = DogfoodRun(
        dogfood_id=generate_dogfood_id(),
        project="karakana",
        skillpack="karakana",
        status="draft",
        created_at="2026-06-10T00:00:00Z",
        command_results=[DogfoodCommandResult(command_id="doctor", command="karakana doctor", status="planned")],
        findings=[DogfoodFinding(finding_id="f1", finding_type="manual_review", title="Review", summary="Review", severity="low")],
        backlog=[DogfoodBacklogItem(item_id="b1", title="Backlog", item_type="manual_review", summary="Review", priority="p3")],
    )

    data = run.to_dict()

    assert "-dogfood-" in run.dogfood_id
    assert data["project"] == "karakana"
    assert data["command_results"][0]["status"] == "planned"


def test_dogfood_schema_rejects_invalid_status():
    with pytest.raises(ValueError):
        DogfoodCommandResult(command_id="bad", command="bad", status="unknown")

