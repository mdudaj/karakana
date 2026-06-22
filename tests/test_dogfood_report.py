from pathlib import Path

from karakana.dogfood.backlog import generate_backlog
from karakana.dogfood.findings import analyze_dogfood
from karakana.dogfood.report import generate_report
from karakana.dogfood.runner import run_dogfood


def test_dogfood_report_includes_decision(tmp_path: Path):
    run, _ = run_dogfood(tmp_path, "karakana", "karakana")
    analyze_dogfood(tmp_path, run.dogfood_id)
    generate_backlog(tmp_path, run.dogfood_id)
    path = generate_report(tmp_path, run.dogfood_id)

    text = path.read_text(encoding="utf-8")
    assert "# Karakana Dogfood Report" in text
    assert "## Decision" in text
    assert "Ready for next dogfood milestone" in text

