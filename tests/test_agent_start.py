from pathlib import Path

from typer.testing import CliRunner

from karakana import __main__ as karakana_main
from karakana.cli import _ensure_project_venv, app
from karakana.handoffs.store import HandoffStore


def write_project_context(root: Path, project: str = "demo", skillpack: str | None = None) -> None:
    skillpack = skillpack or project
    (root / "KARAKANA.md").write_text("# Contract\n", encoding="utf-8")
    memory = root / "ubongo" / "projects" / project
    memory.mkdir(parents=True, exist_ok=True)
    (memory / "overview.md").write_text("# Overview\n", encoding="utf-8")
    (root / "skillpacks").mkdir(exist_ok=True)
    (root / "skillpacks" / f"{skillpack}.yml").write_text(
        f"""name: {skillpack}
description: Test skillpack
version: 0.1.0
status: experimental
project:
  id: {project}
  memory: ubongo/projects/{project}
skills:
  required: [karakana-handoff]
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
    skill_dir = root / "skills" / "karakana-handoff"
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        """---
name: karakana-handoff
description: Test skill
version: 0.1.0
risk_level: low
allowed_tools: [read_file]
requires_approval_for: []
---
# karakana-handoff
""",
        encoding="utf-8",
    )


def test_codex_start_print_only_recovers_and_writes_session_start(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        ["codex", "start", "--project", "demo", "--skillpack", "demo", "--print-only", "--", "--model", "gpt-5.5"],
    )

    assert result.exit_code == 0, result.output
    assert "# Karakana Session Start" in result.output
    assert "Recovered: True" in result.output
    assert "Would launch Codex: codex --model gpt-5.5 '<karakana-session-start-prompt>'" in result.output
    assert (tmp_path / ".karakana" / "session-start.md").read_text(encoding="utf-8").startswith("# Karakana Session Start")
    assert (tmp_path / ".karakana" / "codex-initial-prompt.md").read_text(encoding="utf-8").startswith("Karakana session-start context was loaded before the first user task.")
    handoff = HandoffStore(tmp_path).latest("demo", "demo")
    assert handoff is not None and handoff.recovered is True


def test_codex_start_inline_adds_no_alt_screen_in_print_only(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        ["codex", "start", "--project", "demo", "--skillpack", "demo", "--inline", "--print-only"],
    )

    assert result.exit_code == 0, result.output
    assert "Would launch Codex: codex --no-alt-screen '<karakana-session-start-prompt>'" in result.output


def test_copilot_start_print_only_forwards_args(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        ["copilot", "start", "--project", "demo", "--skillpack", "demo", "--print-only", "--", "--model", "gpt-5.4"],
    )

    assert result.exit_code == 0, result.output
    assert "# Karakana Session Start" in result.output
    assert "Would launch Copilot: copilot --model gpt-5.4" in result.output


def test_agent_start_no_create_fails_without_handoff(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["codex", "start", "--project", "demo", "--skillpack", "demo", "--no-create", "--print-only"])

    assert result.exit_code == 1
    assert "No handoff found for project: demo" in result.output


def test_ensure_project_venv_creates_and_installs_when_missing(tmp_path, monkeypatch):
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        if command[1:3] == ["-m", "venv"]:
            (tmp_path / ".venv" / "bin").mkdir(parents=True)
        return None

    monkeypatch.setattr("karakana.cli.subprocess.run", fake_run)
    monkeypatch.setattr("karakana.cli.sys.executable", "/usr/bin/python")

    created = _ensure_project_venv(tmp_path)

    assert created is True
    assert calls == [
        (["/usr/bin/python", "-m", "venv", str(tmp_path / ".venv")], {"cwd": tmp_path, "check": True}),
        ([str(tmp_path / ".venv" / "bin" / "python"), "-m", "pip", "install", "-e", ".[dev]"], {"cwd": tmp_path, "check": True}),
    ]


def test_ensure_project_venv_skips_existing_environment(tmp_path, monkeypatch):
    venv_python = tmp_path / ".venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("", encoding="utf-8")

    calls = []
    monkeypatch.setattr("karakana.cli.subprocess.run", lambda *args, **kwargs: calls.append((args, kwargs)))

    created = _ensure_project_venv(tmp_path)

    assert created is False
    assert calls == []


def test_codex_start_print_only_does_not_bootstrap(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("karakana.cli._ensure_project_venv", lambda repo_root: (_ for _ in ()).throw(AssertionError("unexpected bootstrap")))

    result = CliRunner().invoke(app, ["codex", "start", "--project", "demo", "--skillpack", "demo", "--print-only"])

    assert result.exit_code == 0, result.output
    assert "Would launch Codex: codex '<karakana-session-start-prompt>'" in result.output


def test_codex_start_flushes_context_before_returning_print_only(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)
    flush_calls = []
    monkeypatch.setattr("karakana.cli._flush_terminal_output", lambda: flush_calls.append("flush"))

    result = CliRunner().invoke(app, ["codex", "start", "--project", "demo", "--skillpack", "demo", "--print-only"])

    assert result.exit_code == 0, result.output
    assert flush_calls == ["flush"]


def test_codex_start_does_not_inject_prompt_for_resume(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["codex", "start", "--project", "demo", "--skillpack", "demo", "--print-only", "--", "resume", "--last"])

    assert result.exit_code == 0, result.output
    assert "Would launch Codex: codex resume --last" in result.output
    assert "karakana-session-start-prompt" not in result.output
    assert not (tmp_path / ".karakana" / "codex-initial-prompt.md").exists()


def test_codex_start_no_inject_prompt_preserves_plain_launch(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["codex", "start", "--project", "demo", "--skillpack", "demo", "--no-inject-prompt", "--print-only"])

    assert result.exit_code == 0, result.output
    assert "Would launch Codex: codex" in result.output
    assert "karakana-session-start-prompt" not in result.output
    assert not (tmp_path / ".karakana" / "codex-initial-prompt.md").exists()


def test_python_module_entrypoint_prebootstraps_missing_venv_for_codex_start(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("KARAKANA_PREBOOTSTRAPPED", raising=False)
    monkeypatch.setattr("karakana.__main__.sys.argv", ["karakana/__main__.py", "codex", "start", "--project", "demo"])
    monkeypatch.setattr("karakana.__main__.sys.executable", "/usr/bin/python")
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        if command[1:3] == ["-m", "venv"]:
            (tmp_path / ".venv" / "bin").mkdir(parents=True)
            (tmp_path / ".venv" / "bin" / "python").write_text("", encoding="utf-8")

    exec_calls = []

    def fake_execv(executable, args):
        exec_calls.append((executable, args))
        raise RuntimeError("exec intercepted")

    monkeypatch.setattr("karakana.__main__.subprocess.run", fake_run)
    monkeypatch.setattr("karakana.__main__.os.execv", fake_execv)

    try:
        try:
            karakana_main.main()
        except RuntimeError as exc:
            assert str(exc) == "exec intercepted"
        else:
            raise AssertionError("expected exec interception")
    finally:
        karakana_main.os.environ.pop("KARAKANA_PREBOOTSTRAPPED", None)

    assert calls == [
        (["/usr/bin/python", "-m", "venv", str(tmp_path / ".venv")], {"cwd": tmp_path, "check": True}),
        ([str(tmp_path / ".venv" / "bin" / "python"), "-m", "pip", "install", "-e", ".[dev]"], {"cwd": tmp_path, "check": True}),
    ]
    assert exec_calls == [
        (
            str(tmp_path / ".venv" / "bin" / "python"),
            [str(tmp_path / ".venv" / "bin" / "python"), "-m", "karakana", "codex", "start", "--project", "demo"],
        )
    ]


def test_python_module_entrypoint_uses_existing_venv_from_system_python(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("KARAKANA_PREBOOTSTRAPPED", raising=False)
    monkeypatch.setattr("karakana.__main__.sys.argv", ["karakana/__main__.py", "codex", "start", "--project", "demo"])
    monkeypatch.setattr("karakana.__main__.sys.executable", "/usr/bin/python3")
    monkeypatch.setattr("karakana.__main__.sys.prefix", "/usr")
    venv_python = tmp_path / ".venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("", encoding="utf-8")
    calls = []
    exec_calls = []

    monkeypatch.setattr("karakana.__main__.subprocess.run", lambda *args, **kwargs: calls.append((args, kwargs)))

    def fake_execv(executable, args):
        exec_calls.append((executable, args))
        raise RuntimeError("exec intercepted")

    monkeypatch.setattr("karakana.__main__.os.execv", fake_execv)

    try:
        try:
            karakana_main.main()
        except RuntimeError as exc:
            assert str(exc) == "exec intercepted"
        else:
            raise AssertionError("expected exec interception")
    finally:
        karakana_main.os.environ.pop("KARAKANA_PREBOOTSTRAPPED", None)

    assert calls == []
    assert exec_calls == [
        (
            str(venv_python),
            [str(venv_python), "-m", "karakana", "codex", "start", "--project", "demo"],
        )
    ]


def test_python_module_entrypoint_does_not_prebootstrap_print_only(monkeypatch):
    monkeypatch.delenv("KARAKANA_PREBOOTSTRAPPED", raising=False)

    assert karakana_main._should_prebootstrap(["codex", "start", "--project", "demo"]) is True
    assert karakana_main._should_prebootstrap(["codex", "start", "--project", "demo", "--print-only"]) is False
    assert karakana_main._should_prebootstrap(["codex", "start", "--project", "demo", "--no-bootstrap"]) is False

    monkeypatch.setenv("KARAKANA_PREBOOTSTRAPPED", "1")
    assert karakana_main._should_prebootstrap(["codex", "start", "--project", "demo"]) is False


def test_python_module_entrypoint_detects_real_project_venv(monkeypatch, tmp_path):
    venv_python = tmp_path / ".venv" / "bin" / "python"

    monkeypatch.setattr("karakana.__main__.sys.prefix", str(tmp_path / ".venv"))
    assert karakana_main._is_running_in_project_venv(venv_python) is True


def test_python_module_entrypoint_does_not_treat_symlink_target_as_project_venv(monkeypatch, tmp_path):
    venv_python = tmp_path / ".venv" / "bin" / "python"

    monkeypatch.setattr("karakana.__main__.sys.prefix", "/usr")
    monkeypatch.setattr("karakana.__main__.sys.executable", "/usr/bin/python3")
    assert karakana_main._is_running_in_project_venv(venv_python) is False
