from pathlib import Path

from karakana.okf.promotion import validate_promotion_record


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
