from karakana.improvement.proposer import ImprovementProposer
from karakana.traces.store import TraceStore


def test_proposer_generates_deterministic_change_from_trace(tmp_path):
    store = TraceStore(tmp_path)
    trace = store.create_run(command="plan", project="karakana", skill="missing", task_type="planning")
    trace.errors.append("Skill not found: skills/missing/SKILL.md")
    trace.finish("failed")
    store.save(trace)

    proposal = ImprovementProposer(tmp_path).propose(project="karakana")

    assert proposal.status == "ready_for_review"
    assert proposal.source_run_ids == [trace.run_id]
    assert proposal.changes
    assert all(change.requires_human_review for change in proposal.changes)
    assert any(change.change_type == "skill_update" for change in proposal.changes)
