from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.protocols.classifier import ProtocolClassifier
from karakana.protocols.loader import ProtocolLoader
from karakana.protocols.resolver import ProtocolResolver
from karakana.protocols.validator import ProtocolValidator
from karakana.skillpacks.loader import SkillpackLoader
from karakana.skillpacks.resolver import SkillpackResolver
from karakana.skillpacks.validator import SkillpackValidator

CORE_PROTOCOLS = {
    "architecture-decision",
    "data-migration",
    "memory-update",
    "python-code-change",
    "release-change",
    "requirements-change",
    "safety-policy-change",
    "skill-update",
    "ux-change",
}


def artifact_kinds(protocol_id: str, conditions: dict | None = None) -> set[str]:
    return {artifact.kind for artifact in ProtocolResolver(Path.cwd()).required_artifacts(protocol_id, conditions or {})}


def test_python_code_change_protocol_loads_and_validates():
    protocol = ProtocolLoader(Path.cwd()).load("python-code-change")
    result = ProtocolValidator(Path.cwd()).validate("python-code-change")

    assert result.ok
    assert protocol.category == "implementation"
    assert "implementer" in protocol.roles
    assert "trace" in {artifact.kind for artifact in protocol.artifacts}


def test_core_protocols_load_and_validate():
    loader = ProtocolLoader(Path.cwd())
    validator = ProtocolValidator(Path.cwd())

    assert CORE_PROTOCOLS <= set(loader.list_protocols())
    for protocol_id in CORE_PROTOCOLS:
        result = validator.validate(protocol_id)
        assert result.ok, result.errors


def test_protocol_artifacts_are_tiered_by_task_conditions():
    base = artifact_kinds("python-code-change")
    behavior = artifact_kinds("python-code-change", {"behavior_change": True, "risk_level": "low"})
    ux = artifact_kinds("python-code-change", {"ux_change": True, "risk_level": "low"})
    architecture = artifact_kinds("python-code-change", {"architecture_change": True, "risk_level": "medium"})
    data = artifact_kinds("python-code-change", {"data_or_migration_change": True, "risk_level": "high"})
    safety = artifact_kinds("python-code-change", {"safety_or_permission_change": True, "risk_level": "high"})

    assert {"task_classification", "trace", "change_summary", "verification_summary", "handoff"} <= base
    assert "requirements_note" not in base
    assert {"requirements_note", "acceptance_criteria", "user_story", "definition_of_done", "test_or_eval_rationale"} <= behavior
    assert {"ux_description", "accessibility_checklist", "screenshot_or_render_evidence"} <= ux
    assert {"adr", "rollback_plan"} <= architecture
    assert {"schema_contract", "migration_plan", "approval_record"} <= data
    assert {"safety_review", "threat_or_abuse_case_note", "approval_record"} <= safety


def test_karakana_skillpack_references_existing_protocols():
    skillpack = SkillpackLoader(Path.cwd()).load("karakana")
    result = SkillpackValidator(Path.cwd()).validate("karakana")
    context = SkillpackResolver(Path.cwd()).resolve_for_project("karakana")

    assert result.ok
    assert skillpack.protocols.default == "python-code-change"
    assert skillpack.protocols.categories["implementation"] == "python-code-change"
    assert skillpack.protocols.categories["requirements"] == "requirements-change"
    assert skillpack.protocols.categories["architecture"] == "architecture-decision"
    assert skillpack.protocols.categories["frontend"] == "ux-change"
    assert skillpack.protocols.categories["migration"] == "data-migration"
    assert skillpack.protocols.categories["safety"] == "safety-policy-change"
    assert skillpack.protocols.categories["skill"] == "skill-update"
    assert skillpack.protocols.categories["memory"] == "memory-update"
    assert skillpack.protocols.categories["release"] == "release-change"
    assert context.protocols["implementation"] == "python-code-change"


def test_protocol_cli_lists_validates_and_resolves_artifacts():
    runner = CliRunner()

    list_result = runner.invoke(app, ["protocol", "list"])
    validate_result = runner.invoke(app, ["protocol", "validate", "python-code-change"])
    artifacts_result = runner.invoke(app, ["protocol", "artifacts", "python-code-change", "--behavior-change", "--ux-change"])

    assert list_result.exit_code == 0
    assert "python-code-change" in list_result.output
    assert validate_result.exit_code == 0
    assert "OK" in validate_result.output
    assert artifacts_result.exit_code == 0
    assert "requirements_note" in artifacts_result.output
    assert "ux_description" in artifacts_result.output


def test_protocol_classifier_resolves_protocol_and_artifacts():
    classification = ProtocolClassifier(Path.cwd()).classify(
        "Implement a Python UX change with database migration and permission checks.",
        project="karakana",
        category="implementation",
    )

    assert classification.protocol_id == "python-code-change"
    assert classification.risk_level == "high"
    assert classification.behavior_change
    assert classification.ux_change
    assert classification.data_or_migration_change
    assert classification.safety_or_permission_change
    assert "requirements_note" in classification.required_artifacts
    assert "ux_description" in classification.required_artifacts
    assert "migration_plan" in classification.required_artifacts
    assert "safety_review" in classification.required_artifacts


def test_protocol_classifier_selects_category_specific_protocols():
    classifier = ProtocolClassifier(Path.cwd())
    cases = {
        "Write requirements and user stories for a new workflow.": "requirements-change",
        "Record an ADR for architecture decisions.": "architecture-decision",
        "Improve the UX of the dashboard page.": "ux-change",
        "Plan a database schema migration.": "data-migration",
        "Update safety policy for permission checks.": "safety-policy-change",
        "Update a Karakana skill with evals.": "skill-update",
        "Update ubongo memory with a new lesson.": "memory-update",
        "Prepare release checklist and version notes.": "release-change",
    }

    for task, protocol_id in cases.items():
        classification = classifier.classify(task, project="karakana")
        assert classification.protocol_id == protocol_id


def test_protocol_artifacts_differ_by_category():
    requirements = artifact_kinds("requirements-change")
    migration = artifact_kinds("data-migration")
    ux = artifact_kinds("ux-change")

    assert "user_story" in requirements
    assert "migration_plan" not in requirements
    assert "migration_plan" in migration
    assert "schema_contract" in migration
    assert "ux_description" in ux
    assert "screenshot_or_render_evidence" in ux


def test_protocol_classify_cli_records_trace_fields(tmp_path, monkeypatch):
    monkeypatch.chdir(Path.cwd())
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "protocol",
            "classify",
            "--task",
            "Implement Python behavior change with UX and permission impact.",
            "--project",
            "karakana",
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert '"protocol_id": "ux-change"' in result.output
    assert '"required_artifacts"' in result.output


def test_protocol_templates_exist():
    root = Path.cwd() / "templates" / "protocols"

    for name in [
        "requirements-note.md",
        "ux-description.md",
        "adr.md",
        "safety-review.md",
        "verification-summary.md",
        "migration-plan.md",
        "schema-contract.md",
        "user-story.md",
    ]:
        assert (root / name).exists()
