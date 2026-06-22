import json

from karakana.actions.schemas import ActionBundle, ActionSource
from karakana.actions.store import ActionStore
from karakana.improvement.schemas import ImprovementProposal, ProposedChange
from karakana.improvement.store import ProposalStore
from karakana.ingestion.sources import load_action_source, load_codex_task_source, load_file_source, load_patch_review_source, load_proposal_source, load_test_run_source, load_trace_source
from karakana.traces.store import TraceStore


def test_source_loading_from_file_trace_action_patch_review_and_proposal(tmp_path):
    (tmp_path / "README.md").write_text("architecture decision command\n", encoding="utf-8")
    source, content, _, _ = load_file_source(tmp_path, tmp_path / "README.md", project="karakana")
    assert source.source_type == "file"
    assert "architecture decision" in content

    trace_store = TraceStore(tmp_path)
    trace = trace_store.create_run(command="demo", project="karakana")
    trace.finish("success")
    trace_store.save(trace)
    trace_source, trace_content, _, _ = load_trace_source(tmp_path, trace.run_id, project="karakana")
    assert trace_source.source_type == "trace"
    assert "demo" in trace_content

    action = ActionBundle(action_run_id="20260101-000000-actions-aaaaaa", status="ready_for_review", created_at="now", source=ActionSource(source_type="model_response"), summary="Update skill checklist")
    ActionStore(tmp_path).save(action)
    action_source, action_content, _, _ = load_action_source(tmp_path, action.action_run_id, project="karakana")
    assert action_source.source_type == "action"
    assert "Update skill" in action_content

    review_dir = tmp_path / ".karakana" / "patch-reviews" / "review-1"
    review_dir.mkdir(parents=True)
    (review_dir / "review.json").write_text(json.dumps({"findings": [{"message": "missing test"}]}), encoding="utf-8")
    patch_source, patch_content, _, _ = load_patch_review_source(tmp_path, "review-1", project="karakana")
    assert patch_source.source_type == "patch_review"
    assert "missing test" in patch_content

    proposal = ImprovementProposal(
        proposal_id="20260101-000000-improve-aaaaaa",
        project="karakana",
        status="ready_for_review",
        created_at="now",
        source_run_ids=["run"],
        summary="Proposal",
        changes=[ProposedChange(target_path="skills/demo/SKILL.md", change_type="skill_update", title="Skill", rationale="Because")],
    )
    ProposalStore(tmp_path).save(proposal)
    proposal_source, proposal_content, _, _ = load_proposal_source(tmp_path, proposal.proposal_id, project="karakana")
    assert proposal_source.source_type == "proposal"
    assert "skill_update" in proposal_content

    codex_dir = tmp_path / ".karakana" / "codex" / "task-1"
    codex_dir.mkdir(parents=True)
    (codex_dir / "codex-task.md").write_text("Write tests for a workflow checklist.\n", encoding="utf-8")
    codex_source, codex_content, _, _ = load_codex_task_source(tmp_path, "task-1", project="karakana")
    assert codex_source.source_type == "codex_task"
    assert "Write tests" in codex_content

    test_dir = tmp_path / ".karakana" / "test-runs" / "test-1"
    test_dir.mkdir(parents=True)
    (test_dir / "result.json").write_text(json.dumps({"exit_code": 1, "stdout": "missing test"}), encoding="utf-8")
    test_source, test_content, _, _ = load_test_run_source(tmp_path, "test-1", project="karakana")
    assert test_source.source_type == "test_run"
    assert "missing test" in test_content
