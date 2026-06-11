from pathlib import Path

from karakana.dogfood.findings import analyze_dogfood
from karakana.dogfood.schemas import DogfoodCommandResult
from karakana.dogfood.summary import DogfoodStore, new_dogfood_run


def test_dogfood_findings_classify_failures_and_warnings(tmp_path: Path):
    run = new_dogfood_run("karakana", "karakana")
    run.command_results = [
        DogfoodCommandResult(command_id="doctor", command="karakana doctor", status="failed", errors=["exit=1"]),
        DogfoodCommandResult(command_id="release", command="karakana release check", status="warning", warnings=["credential warning"]),
    ]
    DogfoodStore(tmp_path).save(run)

    findings, path = analyze_dogfood(tmp_path, run.dogfood_id)

    assert path.exists()
    assert {finding.finding_type for finding in findings} >= {"broken_command", "ux_friction"}

