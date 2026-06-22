import json
from pathlib import Path


def test_codex_session_start_hook_loads_karakana_handoff():
    data = json.loads(Path(".codex/hooks.json").read_text(encoding="utf-8"))

    session_hooks = data["hooks"]["SessionStart"]
    assert session_hooks[0]["matcher"] == "startup|resume"
    hook = session_hooks[0]["hooks"][0]
    assert hook["type"] == "command"
    assert "karakana_session_start.sh" in hook["command"]
    assert hook["statusMessage"] == "Loading Karakana handoff"


def test_karakana_session_start_hook_uses_virtualenv_fallback():
    text = Path(".codex/hooks/karakana_session_start.sh").read_text(encoding="utf-8")

    assert ".venv/bin/karakana" in text
    assert "handoff load --project karakana --skillpack karakana" in text
    assert ".karakana/session-start.md" in text


def test_codex_startup_hook_trust_requirement_is_documented():
    agents = Path("AGENTS.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert ".codex/hooks.json" in agents
    assert "/hooks" in agents
    assert "SessionStart" in readme
    assert "/hooks" in readme
