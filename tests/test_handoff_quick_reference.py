import pytest
from typer.testing import CliRunner

from karakana.cli import app
from karakana.handoffs.builder import create_handoff
from karakana.handoffs.schemas import HandoffArtifact
from karakana.handoffs.store import HandoffStore
from karakana.handoffs.summary import render_session_start
from karakana.handoffs.doctor import diagnose_handoff
from tests.test_session_handoff import write_project_context


def options(source):
    return ["--backlog-position", "R1 / UX stabilisation / form help",
            "--delivery-state", "implemented=local correction",
            "--delivery-state", "verified=focused and browser proof",
            "--delivery-state", "merged=PR116",
            "--delivery-state", "deployed=not performed",
            "--delivery-state", "accepted=target UAT open",
            "--backlog-source", str(source),
            "--backlog-item", "UX-HELP|next|Evidence-form reflow",
            "--backlog-item", "CI|deferred|CRDB GitHub API proof first",
            "--backlog-item", "UAT|blocked|Named actors and approved target"]


@pytest.mark.parametrize("command", ["create", "refresh"])
def test_cli_roundtrip_quick_reference_precedes_complete_brief(tmp_path, monkeypatch, command):
    write_project_context(tmp_path)
    source = tmp_path / "release-backlog.md"
    source.write_text("# R1 backlog\nEvidence form, CI and UAT.\n")
    monkeypatch.chdir(tmp_path)
    brief = "Problem: overlapping hints.\nScope: reusable form flow.\nAcceptance: four widths.\nFirst: capture actual baseline."
    runner = CliRunner()
    result = runner.invoke(app, ["handoff", command, "--project", "demo",
                                "--current-milestone", "PR116 source integrated",
                                "--next-task", "Repair evidence-form flow",
                                "--next-task-brief", brief, *options(source)])
    assert result.exit_code == 0, result.output
    handoff = HandoffStore(tmp_path).latest("demo")
    metadata = handoff.continuation["quick_reference"]
    assert metadata["position"] == "R1 / UX stabilisation / form help"
    assert metadata["delivery_state"]["merged"] == "PR116"
    assert metadata["backlog"]["items"][1]["state"] == "deferred"
    assert metadata["backlog"]["source"] == str(source)
    assert str(source) in handoff.reference_artifacts
    loaded = runner.invoke(app, ["handoff", "load", "--project", "demo", "--no-okf-context"])
    assert loaded.exit_code == 0, loaded.output
    markdown = (HandoffStore(tmp_path).run_dir(handoff.handoff_id) / "handoff.md").read_text()
    for text in (loaded.output, markdown):
        assert text.index("## Quick Reference") < text.index("## Next Task Brief")
        assert brief in text
        assert "Evidence-form reflow" in text and "CRDB GitHub API proof first" in text
        assert "target UAT open" in text and "not performed" in text
        assert "Snapshot" in text and str(source) in text
    assert "--details" in loaded.output
    assert "## Do Not Reread Unless Needed" not in loaded.output
    detailed = runner.invoke(app, ["handoff", "load", "--project", "demo", "--details", "--no-okf-context"])
    assert detailed.exit_code == 0 and "## Do Not Reread Unless Needed" in detailed.output
    assert brief in detailed.output and "Recommendation only" in loaded.output


def test_source_change_missing_and_refresh_preserve_history(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    source = tmp_path / "backlog.md"
    source.write_text("Original reviewed source")
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    assert runner.invoke(app, ["handoff", "create", "--project", "demo", *options(source)]).exit_code == 0
    store = HandoffStore(tmp_path)
    first = store.latest("demo")
    old = {p.name: p.read_bytes() for p in store.run_dir(first.handoff_id).iterdir()}
    source.write_text("Changed source, no longer the reviewed snapshot")
    changed = runner.invoke(app, ["handoff", "load", "--project", "demo", "--no-okf-context"])
    assert changed.exit_code == 0 and "Backlog source changed" in changed.output
    assert "deferred" in changed.output
    doctor = diagnose_handoff(tmp_path, "demo")
    assert doctor.status == "warning" and not doctor.checks["backlog_snapshot_current"]
    source.unlink()
    missing = runner.invoke(app, ["handoff", "load", "--project", "demo", "--no-okf-context"])
    assert missing.exit_code == 0 and "Backlog source missing" in missing.output
    refreshed = runner.invoke(app, ["handoff", "refresh", "--project", "demo",
                                    "--current-milestone", "Unverified follow-up", "--no-recover-artifacts"])
    assert refreshed.exit_code == 0, refreshed.output
    assert store.latest("demo").previous_handoff_id == first.handoff_id
    assert {p.name: p.read_bytes() for p in store.run_dir(first.handoff_id).iterdir()} == old


@pytest.mark.parametrize("args", [
    ["--delivery-state", "finished=yes"],
    ["--delivery-state", "merged=yes", "--delivery-state", "merged=no"],
    ["--backlog-item", "UX|next|No source"],
    ["--backlog-item", "missing-parts"],
    ["--backlog-source", "missing.md"],
])
def test_invalid_quick_reference_is_not_persisted(tmp_path, monkeypatch, args):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["handoff", "create", "--project", "demo", *args])
    assert result.exit_code != 0
    assert HandoffStore(tmp_path).latest("demo") is None


def test_legacy_unknowns_redaction_and_project_scoping(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    write_project_context(tmp_path, "other")
    source = tmp_path / "backlog.md"
    source.write_text("Current source")
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(app, ["handoff", "create", "--project", "demo", *options(source),
                                "--from-note", "Do not dump this historical narrative"])
    assert result.exit_code == 0, result.output
    handoff = HandoffStore(tmp_path).latest("demo")
    legacy = handoff.to_dict()
    legacy["continuation"].pop("quick_reference")
    restored = HandoffArtifact.from_dict(legacy)
    text = render_session_start(restored, "handoff.md")
    assert "Not recorded" in text and "Do not dump this historical narrative" not in text
    assert set(create_handoff(tmp_path, "demo").to_dict()) == set(handoff.to_dict())
    legacy["continuation"]["quick_reference"] = {
        "position": "token=syntheticprivatevalue", "delivery_state": {"verified": "password=otherprivatevalue"},
        "backlog": {"items": [{"id": "SAFE", "state": "next", "summary": "secret=thirdprivatevalue"}]}}
    safe = render_session_start(HandoffArtifact.from_dict(legacy), "handoff.md")
    assert all(value not in safe for value in ("syntheticprivatevalue", "otherprivatevalue", "thirdprivatevalue"))
    other = runner.invoke(app, ["handoff", "load", "--project", "other", "--no-create", "--no-okf-context"])
    assert other.exit_code == 1 and "Evidence-form reflow" not in other.output


def test_explicit_source_supersedes_generic_memory_backlog(tmp_path):
    write_project_context(tmp_path)
    generic = tmp_path / "ubongo/projects/demo/open-issues.md"
    generic.write_text("- [ ] Old bootstrap work\n")
    source = tmp_path / "current.md"
    source.write_text("Current R1 queue")
    handoff = create_handoff(tmp_path, "demo", backlog_source=str(source),
                             backlog_items=["UX|next|Current control correction"])
    assert str(source) in handoff.inspect_first
    assert str(generic) not in handoff.reference_artifacts
    assert "Old bootstrap work" not in render_session_start(handoff, "handoff.md")


@pytest.mark.parametrize("payload", ["unexpected", {"backlog": []}, {"backlog": {"items": [None]}}])
def test_invalid_snapshot_warns_without_crashing_or_claiming_completion(tmp_path, payload):
    write_project_context(tmp_path)
    handoff = create_handoff(tmp_path, "demo")
    handoff.continuation["quick_reference"] = payload
    rendered = render_session_start(handoff, "handoff.md")
    assert "invalid" in rendered and "Not recorded" in rendered


def test_table_text_is_safe_and_age_warnings_are_visible(tmp_path):
    write_project_context(tmp_path)
    handoff = create_handoff(tmp_path, "demo", backlog_position="R1 | UX\n<script>\x1b[31m")
    handoff.updated_at = "2020-01-01T00:00:00+00:00"
    text = render_session_start(handoff, "handoff.md")
    assert "R1 \\| UX" in text and "<script>" not in text and "\x1b" not in text
    assert "older than 7 days" in text
    assert "Not recorded" in text and "%" not in text


def test_attention_preserves_findings_and_failure_but_not_success_notice(tmp_path):
    write_project_context(tmp_path)
    handoff = create_handoff(tmp_path, "demo")
    handoff.open_findings = ["P1: verify the target actor before acceptance."]
    handoff.warnings = ["Protocol check good for trace alpha is passed.",
                        "Protocol check bad for trace beta is missing evidence."]
    text = render_session_start(handoff, "handoff.md")
    assert text.index("P1: verify") < text.index("## Next Task Brief")
    assert "missing evidence" in text and "Protocol check good" not in text
