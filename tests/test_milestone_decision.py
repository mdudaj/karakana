import json
from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.dogfood.schemas import DogfoodBacklogItem, DogfoodRun
from karakana.dogfood.summary import DogfoodStore
from karakana.milestones.decision import generate_next_milestone
from karakana.milestones.store import MilestoneStore
from karakana.handoffs.store import HandoffStore
from karakana.codex.patch import PatchCapture
from karakana.codex.reviewer import PatchReviewer
from karakana.skills.validator import SkillValidator


CURRENT_STATE_NOTE = (
    "Slice 1 was implemented, but dashboard reports 0 registered Tier 1 sources and no snapshot captured. "
    "There is no action button or menu for curriculum intake management. Need better UX for users to "
    "provide TIE links and run retrieval actions."
)


def write_project_context(root: Path, project: str = "msc-platform") -> None:
    memory = root / "ubongo" / "projects" / project
    memory.mkdir(parents=True)
    (memory / "overview.md").write_text("# Project\n\nCurrent project context.\n", encoding="utf-8")
    skillpacks = root / "skillpacks"
    skillpacks.mkdir()
    (skillpacks / f"{project}.yml").write_text(
        f"""name: {project}
description: Test project profile
version: 0.1.0
status: experimental
project:
  id: {project}
  memory: ubongo/projects/{project}
skills:
  required: []
  optional: []
model_routes: {{}}
safety:
  high_risk_paths: []
  blocked_paths: []
  requires_approval_for: []
tests:
  commands: [pytest]
  recommended_before_commit: []
conventions:
  notes: []
""",
        encoding="utf-8",
    )


def test_next_milestone_skill_validates():
    result = SkillValidator().validate(Path("skills/next-milestone-decision"))

    assert result.errors == []
    assert result.warnings == []


def test_msc_platform_skillpack_includes_next_milestone_skill():
    text = Path("skillpacks/msc-platform.yml").read_text(encoding="utf-8")

    assert "next-milestone-decision" in text


def test_cli_creates_decision_and_copy_ready_instructions(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        [
            "milestone",
            "next",
            "--project",
            "msc-platform",
            "--skillpack",
            "msc-platform",
            "--from-note",
            CURRENT_STATE_NOTE,
            "--write-instructions",
        ],
    )

    assert result.exit_code == 0, result.output
    run_id = next(line.split(":", 1)[1].strip() for line in result.output.splitlines() if line.startswith("Milestone run ID:"))
    run_dir = tmp_path / ".karakana" / "milestones" / run_id
    markdown = (run_dir / "next-milestone.md").read_text(encoding="utf-8")
    instructions = (run_dir / "instructions.md").read_text(encoding="utf-8")

    for heading in (
        "## Current State Summary",
        "## Candidate Milestones",
        "## Recommended Milestone",
        "## Generated Instructions",
        "## Verification Plan",
        "## Definition of Done",
    ):
        assert heading in markdown
    assert CURRENT_STATE_NOTE in markdown
    assert "Slice 1.1: Curriculum Intake Management UX and TIE Source Actions" in markdown
    assert "Do not push or deploy" in instructions
    assert (run_dir / "next-milestone.json").exists()
    assert HandoffStore(tmp_path).latest("msc-platform", "msc-platform") is not None


def test_from_note_influences_state_and_no_brainstorm_is_deterministic(tmp_path):
    write_project_context(tmp_path)

    decision = generate_next_milestone(
        tmp_path,
        project="msc-platform",
        skillpack="msc-platform",
        from_note=CURRENT_STATE_NOTE,
        no_brainstorm=True,
    )

    assert CURRENT_STATE_NOTE in decision.current_state_summary
    assert decision.brainstorm_used is False
    assert decision.recommended_milestone == "Slice 1.1: Curriculum Intake Management UX and TIE Source Actions"
    assert round(sum(candidate.decision_weight for candidate in decision.candidates), 4) == 1.0
    assert decision.sensitivity.scenarios_tested == 21
    assert decision.sensitivity.robust is False
    assert "Requirements Elicitation and Specification Regeneration" in decision.sensitivity.alternate_winners
    assert decision.sensitivity.critical_criteria


def test_strict_mode_blocks_unresolved_p1_and_writes_artifact(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    DogfoodStore(tmp_path).save(
        DogfoodRun(
            dogfood_id="dogfood-p1",
            project="msc-platform",
            skillpack="msc-platform",
            status="completed_with_warnings",
            created_at="2026-06-18T00:00:00+00:00",
            backlog=[
                DogfoodBacklogItem(
                    item_id="backlog-p1",
                    title="Resolve planning gap",
                    item_type="manual_review",
                    summary="Planning evidence is incomplete.",
                    priority="p1",
                )
            ],
        )
    )
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        ["milestone", "next", "--project", "msc-platform", "--skillpack", "msc-platform", "--strict"],
    )

    assert result.exit_code == 1
    assert "P1 dogfood backlog: Resolve planning gap" in result.output
    run_id = next(line.split(":", 1)[1].strip() for line in result.output.splitlines() if line.startswith("Milestone run ID:"))
    data = json.loads((MilestoneStore(tmp_path).run_dir(run_id) / "next-milestone.json").read_text(encoding="utf-8"))
    assert data["blocked"] is True
    assert any("P1 dogfood backlog" in blocker for blocker in data["blockers"])


def test_generated_instructions_preserve_safety_gates(tmp_path):
    write_project_context(tmp_path)

    decision = generate_next_milestone(tmp_path, project="msc-platform", skillpack="msc-platform", from_note=CURRENT_STATE_NOTE)

    assert "Do not push or deploy unless explicitly approved" in decision.generated_instructions
    assert "patch-review" in decision.generated_instructions
    assert "P0/P1" in decision.generated_instructions


def test_milestone_uses_only_project_scoped_patch_evidence(tmp_path):
    import subprocess

    write_project_context(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    scoped = PatchCapture(tmp_path).capture_diff(project="msc-platform", skillpack="msc-platform")
    PatchReviewer(tmp_path).review_diff(tmp_path / ".karakana" / "patches" / scoped.patch_run_id / "changes.diff")

    decision = generate_next_milestone(tmp_path, project="msc-platform", skillpack="msc-platform", from_note=CURRENT_STATE_NOTE)

    patch_evidence = [item for item in decision.evidence if item.source_type == "patch_review"]
    assert len(patch_evidence) == 1
    assert patch_evidence[0].source_id is not None
    assert "advisory" not in patch_evidence[0].summary


def test_low_relevance_ingestion_findings_do_not_pollute_decision(tmp_path):
    from karakana.ingestion.schemas import IngestionBundle, IngestionCandidate
    from karakana.ingestion.store import IngestionStore

    write_project_context(tmp_path)
    IngestionStore(tmp_path).save(
        IngestionBundle(
            ingest_id="ingest-unrelated",
            project="msc-platform",
            skillpack="msc-platform",
            status="ready_for_review",
            created_at="2026-06-18T00:00:00+00:00",
            candidates=[
                IngestionCandidate(
                    candidate_id="candidate-whatsapp",
                    candidate_type="whatsapp_evaluator_channel",
                    title="Add WhatsApp evaluator reminders",
                    summary="Configure evaluator reminder delivery.",
                    risk_level="high",
                )
            ],
        )
    )

    decision = generate_next_milestone(tmp_path, project="msc-platform", skillpack="msc-platform", from_note=CURRENT_STATE_NOTE)

    assert all("WhatsApp" not in finding for finding in decision.open_findings)


def test_candidate_artifact_exposes_mcda_scores_and_sensitivity(tmp_path):
    write_project_context(tmp_path)

    decision = generate_next_milestone(
        tmp_path,
        project="msc-platform",
        skillpack="msc-platform",
        from_note=CURRENT_STATE_NOTE,
    )

    candidate = decision.candidates[0]
    assert candidate.decision_score > 0
    assert set(candidate.criterion_scores) == {criterion.name for criterion in decision.criteria}
    assert "probability" not in candidate.to_dict()
    assert decision.sensitivity.baseline_winner == decision.recommended_milestone


def test_explicit_foreign_dogfood_is_rejected(tmp_path):
    write_project_context(tmp_path)
    DogfoodStore(tmp_path).save(
        DogfoodRun(
            dogfood_id="dogfood-foreign",
            project="another-project",
            skillpack="another-project",
            status="completed",
            created_at="2026-06-18T00:00:00+00:00",
        )
    )

    decision = generate_next_milestone(
        tmp_path,
        project="msc-platform",
        skillpack="msc-platform",
        from_dogfood="dogfood-foreign",
        from_note=CURRENT_STATE_NOTE,
        strict=True,
    )

    assert decision.blocked is True
    assert "Dogfood project mismatch: expected msc-platform, found another-project." in decision.blockers
    assert all(item.source_type != "dogfood" for item in decision.evidence)


def test_previous_milestone_evidence_is_project_scoped(tmp_path):
    write_project_context(tmp_path)
    other = generate_next_milestone(tmp_path, project="msc-platform", skillpack="msc-platform")
    other.project = "another-project"
    MilestoneStore(tmp_path).save(other)

    decision = generate_next_milestone(
        tmp_path,
        project="msc-platform",
        skillpack="msc-platform",
        from_note=CURRENT_STATE_NOTE,
    )

    assert all(item.source_type != "previous_milestone" for item in decision.evidence)
