from karakana.improvement.analyzer import TraceAnalyzer
from karakana.traces.store import TraceStore


def save_trace(tmp_path, command="plan", status="failed", project="karakana", skill="missing"):
    store = TraceStore(tmp_path)
    trace = store.create_run(command=command, project=project, skill=skill, task_type="planning")
    trace.errors.append("Skill not found: skills/missing/SKILL.md")
    trace.finish(status)
    store.save(trace)
    return trace


def test_analyze_no_traces(tmp_path):
    result = TraceAnalyzer(tmp_path).analyze(project="karakana")

    assert result.findings == []
    assert result.warnings


def test_analyze_failed_trace_generates_findings(tmp_path):
    trace = save_trace(tmp_path)

    result = TraceAnalyzer(tmp_path).analyze(project="karakana")

    assert trace.run_id in result.source_run_ids
    assert any(finding.finding_type == "missing_skill" for finding in result.findings)
    assert any(finding.finding_type == "missing_eval" for finding in result.findings)


def test_analyze_warning_trace_generates_documentation_gap(tmp_path):
    store = TraceStore(tmp_path)
    trace = store.create_run(command="memory validate", project="karakana")
    trace.warnings.append("Something needs documentation")
    trace.finish("success")
    store.save(trace)

    result = TraceAnalyzer(tmp_path).analyze(project="karakana")

    assert any(finding.finding_type == "documentation_gap" for finding in result.findings)


def test_analyze_repeated_failure(tmp_path):
    save_trace(tmp_path, command="plan")
    save_trace(tmp_path, command="plan")

    result = TraceAnalyzer(tmp_path).analyze(project="karakana")

    assert any(finding.title == "Repeated failures in plan" for finding in result.findings)
