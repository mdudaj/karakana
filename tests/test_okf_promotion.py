from pathlib import Path

from karakana.okf.promotion import classify_promotion_candidate
from karakana.okf.promotion import scan_promotion_candidates
from karakana.okf.promotion import validate_promotion_record
from karakana.okf.promotion import write_promotion_proposal


def test_validate_promotion_record_accepts_reviewable_record(tmp_path):
    (tmp_path / ".karakana/handoffs/example").mkdir(parents=True)
    (tmp_path / ".karakana/handoffs/example/handoff.md").write_text("# handoff\n", encoding="utf-8")
    record = tmp_path / "promotion.yml"
    record.write_text(
        "\n".join(
            [
                "source_artifact: .karakana/handoffs/example/handoff.md",
                "concept_id: sample.handoff",
                "reason: Promote stable handoff lesson",
                "reviewer: user",
                "date: 2026-06-22",
                "verification: karakana okf validate",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = validate_promotion_record(tmp_path, Path("promotion.yml"))

    assert result.ok
    assert result.warnings == []


def test_validate_promotion_record_rejects_missing_fields(tmp_path):
    record = tmp_path / "promotion.yml"
    record.write_text("source_artifact: .karakana/handoff.md\n", encoding="utf-8")

    result = validate_promotion_record(tmp_path, record)

    assert not result.ok
    assert "Missing required field: concept_id" in result.errors
    assert "Missing required field: reason" in result.errors


def test_validate_promotion_record_rejects_blocked_source(tmp_path):
    record = tmp_path / "promotion.yml"
    record.write_text(
        "\n".join(
            [
                "source_artifact: .env",
                "concept_id: sample.secret",
                "reason: unsafe",
                "reviewer: user",
                "date: 2026-06-22",
                "verification: none",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = validate_promotion_record(tmp_path, record)

    assert not result.ok
    assert "Blocked source artifact: .env" in result.errors


def test_scan_promotion_candidates_classifies_ready_requirement(tmp_path):
    req = tmp_path / ".karakana/requirements/req-demo"
    req.mkdir(parents=True)
    (req / "prd.md").write_text("# PRD\n", encoding="utf-8")
    (req / "readiness.md").write_text("Ready: True\nStatus: ready\n", encoding="utf-8")

    candidates = scan_promotion_candidates(tmp_path, [Path(".karakana/requirements")])

    prd = next(candidate for candidate in candidates if candidate.source_artifact.endswith("prd.md"))
    assert prd.eligible is True
    assert prd.suggested_type == "Requirement"


def test_classify_promotion_candidate_rejects_raw_trace(tmp_path):
    trace = tmp_path / ".karakana/traces/run/trace.json"
    trace.parent.mkdir(parents=True)
    trace.write_text("{}", encoding="utf-8")

    candidate = classify_promotion_candidate(tmp_path, trace)

    assert candidate.eligible is False
    assert "runtime evidence" in candidate.reason


def test_write_promotion_proposal_writes_concept_and_record(tmp_path):
    adr_dir = tmp_path / "docs/adr"
    adr_dir.mkdir(parents=True)
    artifact = adr_dir / "0001-demo.md"
    artifact.write_text("# ADR\n", encoding="utf-8")

    proposal = write_promotion_proposal(tmp_path, artifact, reviewer="reviewer@example.com")

    assert proposal.concept_path.exists()
    assert proposal.promotion_record_path.exists()
    assert "status: proposed" in proposal.concept_path.read_text(encoding="utf-8")
    result = validate_promotion_record(tmp_path, proposal.promotion_record_path)
    assert result.ok
