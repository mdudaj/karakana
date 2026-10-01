from typer.testing import CliRunner

from karakana.cli import app
from karakana.requirements.schemas import UserStory
from karakana.requirements.store import RequirementsStore
from karakana.requirements.stories import LEGACY_TEMPLATE_SLICES, is_legacy_template_stories


def test_requirements_cli_prd_stories_issues_ready_show_publish(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["requirements", "prd", "--from-note", "Add a safe requirements layer", "--project", "karakana", "--no-current-skillpack"])

    assert result.exit_code == 0
    assert "Requirement ID:" in result.output
    req_id = [line.split(":", 1)[1].strip() for line in result.output.splitlines() if line.startswith("Requirement ID:")][0]

    stories = CliRunner().invoke(app, ["requirements", "stories", "--from-prd", req_id])
    assert stories.exit_code == 0
    assert "Stories:" in stories.output

    issues = CliRunner().invoke(app, ["requirements", "issues", "--from-prd", req_id])
    assert issues.exit_code == 0
    assert "Issues:" in issues.output

    ready = CliRunner().invoke(app, ["requirements", "ready", req_id])
    assert ready.exit_code == 0
    assert "Status: not_ready" in ready.output
    assert "Ready: False" in ready.output

    show = CliRunner().invoke(app, ["requirements", "show", req_id])
    assert show.exit_code == 0
    assert "Requirement ID" in show.output

    publish = CliRunner().invoke(app, ["requirements", "publish", req_id])
    assert publish.exit_code == 0
    assert "Dry run" in publish.output


def test_requirements_cli_structured_source_is_ready(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    seed = """## Specification / PRD Seed
Problem: Project handoffs omit active development items.
Goal: Link active project backlog items from each handoff.
Functional requirements:
- Handoffs include only their own project's active backlog path.
Acceptance criteria:
- Completed-only backlogs are omitted from handoffs.
"""

    generated = CliRunner().invoke(app, ["requirements", "prd", "--from-note", seed, "--project", "karakana", "--no-current-skillpack"])
    assert generated.exit_code == 0
    req_id = [line.split(":", 1)[1].strip() for line in generated.output.splitlines() if line.startswith("Requirement ID:")][0]

    stories = CliRunner().invoke(app, ["requirements", "stories", "--from-prd", req_id])
    issues = CliRunner().invoke(app, ["requirements", "issues", "--from-prd", req_id])
    assert stories.exit_code == 0
    assert issues.exit_code == 0
    req_dir = tmp_path / ".karakana" / "requirements" / req_id
    assert "Handoffs include only their own project's active backlog path." in (req_dir / "stories.md").read_text(encoding="utf-8")
    assert "Completed-only backlogs are omitted from handoffs." in (req_dir / "issues.md").read_text(encoding="utf-8")
    assert "the capability described by this PRD" not in (req_dir / "prd.md").read_text(encoding="utf-8")

    ready = CliRunner().invoke(app, ["requirements", "ready", req_id, "--json"])

    assert ready.exit_code == 0
    assert "Ready: True" in ready.output
    assert '"failed": []' in ready.output


def test_requirements_issues_refreshes_only_known_legacy_template_stories(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = """## Specification / PRD Seed
Goal: Show active project backlog links in handoffs.
Functional requirements:
- Handoffs link their own project's active backlog.
Acceptance criteria:
- The handoff includes the correct project backlog link.
"""
    generated = CliRunner().invoke(app, ["requirements", "prd", "--from-note", source, "--no-current-skillpack"])
    assert generated.exit_code == 0
    req_id = [line.split(":", 1)[1].strip() for line in generated.output.splitlines() if line.startswith("Requirement ID:")][0]
    store = RequirementsStore(tmp_path)
    prd = store.load_prd(req_id)
    old_stories = [
        UserStory(
            story_id=f"{req_id}-story-{index}", req_id=req_id, title=f"{prd.title}: {title}",
            actor="developer", want=want, outcome="the work can move forward without vague implementation tasks",
            acceptance_criteria=[
                f"Given the PRD, when {title} is implemented, then artifacts remain reviewable.",
                "Given missing information, when readiness runs, then gaps are reported.",
            ],
            standards=list(prd.standards_spec.standards),
            risks=list(prd.risks),
            required_skills=list(prd.suggested_skills),
            required_tests_or_evals=list(prd.test_and_eval_plan),
            definition_of_ready=["PRD exists.", "Acceptance criteria exist.", "Safety constraints are listed.", "Model route is recommended."],
            definition_of_done=["Tests and evals pass.", "Artifacts are generated under .karakana/requirements/.", "Human review remains required before publishing or execution."],
            risk_level="high" if any("High-risk" in item for item in prd.safety_constraints) else "medium",
        )
        for index, (title, want) in enumerate(LEGACY_TEMPLATE_SLICES, start=1)
    ]
    assert is_legacy_template_stories(prd, old_stories)
    old_stories[0].acceptance_criteria.append("Reviewer-edited criterion.")
    assert not is_legacy_template_stories(prd, old_stories)
    store.save_stories(req_id, old_stories)
    blocked = CliRunner().invoke(app, ["requirements", "issues", "--from-prd", req_id])
    assert blocked.exit_code == 1
    assert "contain edits" in blocked.output
    assert store.load_stories(req_id)[0].acceptance_criteria[-1] == "Reviewer-edited criterion."
    old_stories[0].acceptance_criteria.pop()
    store.save_stories(req_id, old_stories)

    issues = CliRunner().invoke(app, ["requirements", "issues", "--from-prd", req_id])

    assert issues.exit_code == 0
    assert "Older template stories were regenerated" in issues.output
    assert [story.want for story in store.load_stories(req_id)] == ["Handoffs link their own project's active backlog."]
    assert [issue.scope for issue in store.load_issues(req_id)] == [["Handoffs link their own project's active backlog."]]
