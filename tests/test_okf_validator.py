from pathlib import Path

from karakana.okf.parser import parse_concept_file
from karakana.okf.validator import OkfValidator


def write_concept(root: Path, relative: str, frontmatter: str, body: str = "# Concept\n") -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter}---\n\n{body}", encoding="utf-8")
    return path


def valid_frontmatter(**overrides):
    data = {
        "id": "sample.project",
        "type": "Project",
        "title": "Sample Project",
        "status": "active",
        "owner": "sample",
        "project": "sample",
        "summary": "Sample concept.",
        "source": "README.md",
        "tags": ["sample"],
        "updated": "2026-06-22",
    }
    data.update(overrides)
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {item}" for item in value)
        elif isinstance(value, dict):
            lines.append(f"{key}:")
            for child_key, child_values in value.items():
                lines.append(f"  {child_key}:")
                lines.extend(f"    - {item}" for item in child_values)
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def test_parse_concept_file_reads_frontmatter(tmp_path):
    (tmp_path / "README.md").write_text("# sample\n", encoding="utf-8")
    path = write_concept(tmp_path, "okf/sample.md", valid_frontmatter())

    concept = parse_concept_file(path)

    assert concept.concept_id == "sample.project"
    assert concept.concept_type == "Project"
    assert "sample" in concept.tags


def test_validator_accepts_curated_repository_bundle():
    result = OkfValidator(Path.cwd()).validate()

    assert result.ok
    assert result.counts_by_project["karakana"] >= 8
    assert result.counts_by_project["msc-platform"] >= 6
    assert result.counts_by_type["Project"] >= 2
    assert result.counts_by_type["WorkProtocol"] >= 6
    assert result.counts_by_type["Verification"] >= 2


def test_validator_rejects_missing_type(tmp_path):
    (tmp_path / "README.md").write_text("# sample\n", encoding="utf-8")
    write_concept(tmp_path, "okf/missing-type.md", valid_frontmatter(type=""))

    result = OkfValidator(tmp_path).validate()

    assert not result.ok
    assert any("Missing required field: type" in issue.message for issue in result.errors)


def test_validator_rejects_unknown_type(tmp_path):
    (tmp_path / "README.md").write_text("# sample\n", encoding="utf-8")
    write_concept(tmp_path, "okf/unknown-type.md", valid_frontmatter(type="MadeUp"))

    result = OkfValidator(tmp_path).validate()

    assert not result.ok
    assert any("Unknown type: MadeUp" in issue.message for issue in result.errors)


def test_validator_warns_on_unresolved_relationship(tmp_path):
    (tmp_path / "README.md").write_text("# sample\n", encoding="utf-8")
    write_concept(
        tmp_path,
        "okf/relationship.md",
        valid_frontmatter(relationships={"related_to": ["sample.missing"]}),
    )

    result = OkfValidator(tmp_path).validate()

    assert result.ok
    assert any("Unresolved relationship target: sample.missing" in issue.message for issue in result.warnings)


def test_validator_rejects_blocked_source_path(tmp_path):
    write_concept(tmp_path, "okf/secret.md", valid_frontmatter(source=".env"))

    result = OkfValidator(tmp_path).validate()

    assert not result.ok
    assert any("Blocked source path: .env" in issue.message for issue in result.errors)


def test_validator_rejects_cross_project_id_without_matching_prefix(tmp_path):
    (tmp_path / "README.md").write_text("# sample\n", encoding="utf-8")
    write_concept(tmp_path, "okf/wrong-project.md", valid_frontmatter(id="other.project"))

    result = OkfValidator(tmp_path).validate()

    assert not result.ok
    assert any("id must start with project prefix 'sample.'" in issue.message for issue in result.errors)


def test_strict_mode_escalates_warnings(tmp_path):
    write_concept(tmp_path, "okf/missing-source.md", valid_frontmatter(source="missing.md"))

    result = OkfValidator(tmp_path).validate(strict=True)

    assert not result.ok
    assert any("Source path does not exist: missing.md" in issue.message for issue in result.errors)
