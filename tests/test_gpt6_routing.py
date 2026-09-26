import json
from types import SimpleNamespace

import pytest

from karakana.codex.executor import CodexExecution
from karakana.models.router import DEFAULT_MODEL_ROUTING, route_model
from karakana.tools.codex_executor import _recommended_codex_route
from karakana.models.escalation import recommend_escalation
from karakana.safety.model_routing import validate_model_route
from karakana.skillpacks.loader import SkillpackLoader
from pathlib import Path


@pytest.mark.parametrize("task,model,effort", [
    ("planning", "gpt-6-sol", "medium"),
    ("routine_code_implementation", "gpt-6-luna", "high"),
    ("documentation", "gpt-6-luna", "high"),
    ("refactoring", "gpt-6-sol", "medium"),
    ("security_or_auth_change", "gpt-6-sol", "high"),
    ("database_or_index_migration", "gpt-6-sol", "high"),
])
def test_capability_and_effort(task, model, effort):
    route = route_model(task)
    assert (route["model"], route["reasoning_effort"]) == (model, effort)
    assert route["availability_verified"] is False
    assert route["fallback_model"] == model.replace("gpt-6", "gpt-5.6")
    assert not validate_model_route(task, "openai_codex", model)


def test_astra_is_explicit_not_default():
    assert all(route["model"] != "gpt-6-astra" for route in DEFAULT_MODEL_ROUTING.values())
    route = route_model("high_risk_code_review", model="gpt-6-astra")
    assert route["manual_override"] and route["requires_explicit_selection"]
    assert route["reasoning_effort"] == "low"
    assert validate_model_route("high_risk_code_review", "openai_codex", "gpt-6-astra", "high")


def test_legacy_luna_is_not_safe_principal_fallback():
    assert route_model("documentation", model="gpt-5.6-luna")["capability_tier"] == "routine_coding"
    assert validate_model_route("model_routing_planning", "openai_codex", "gpt-5.6-luna", "high")


def test_prompt_routes_actual_task_not_all_skill_approval_domains():
    assert _recommended_codex_route("Write parser tests", ["authentication_change"])["model"] == "gpt-6-luna"
    assert _recommended_codex_route("Refactor multiple files", [])["model"] == "gpt-6-sol"
    assert _recommended_codex_route("Implement reflection trace schema", [])["role"] == "routine_implementer"


def test_two_attempt_escalation_is_advisory_and_no_first_failure_jump():
    assert not recommend_escalation("openai_codex", "gpt-6-luna", ["tests_fail_after_first_patch"])["should_escalate"]
    result = recommend_escalation("openai_codex", "gpt-6-luna", ["repeated_failure_after_two_attempts"])
    assert result["to_model"] == "gpt-6-sol"
    result = recommend_escalation("openai_codex", "gpt-6-sol", ["repeated_failure_after_two_attempts"])
    assert result["to_model"] == "gpt-6-astra"
    assert result["requires_explicit_selection"]


def test_bundled_project_defaults_are_current():
    loader = SkillpackLoader(Path(__file__).resolve().parents[1])
    for name in loader.list_skillpacks():
        pack = loader.load(name)
        for task, override in pack.to_dict()["model_routes"].items():
            assert override["model"] in {"gpt-6-sol", "gpt-6-luna"}, (name, task)
            if task == "planning":
                assert override["model"] == "gpt-6-sol", name


def test_executor_passes_effort_and_reports_failure(tmp_path, monkeypatch):
    task = tmp_path / ".karakana" / "codex-task.md"
    task.parent.mkdir()
    task.write_text("Write export tests")
    task.with_suffix(".json").write_text(json.dumps({
        "recommended_provider": "openai_codex", "recommended_model": "gpt-6-luna",
        "reasoning_effort": "high",
    }))
    monkeypatch.setattr("karakana.codex.executor._git_branch", lambda root: "feature/test")
    monkeypatch.setattr("karakana.codex.executor.shutil.which", lambda name: "/bin/codex")

    def run(command, **kwargs):
        assert command == ["/bin/codex", "exec", "--model", "gpt-6-luna", "-c", 'model_reasoning_effort="high"', "-"]
        return SimpleNamespace(returncode=7, stdout="", stderr="model unavailable")

    monkeypatch.setattr("karakana.codex.executor.subprocess.run", run)
    with pytest.raises(RuntimeError, match="exit code 7"):
        CodexExecution(tmp_path).execute(task, explicit=True)
