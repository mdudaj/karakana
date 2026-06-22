import json

from karakana.tools.github import (
    detect_github_context,
    get_actor,
    get_event_path,
    get_ref_name,
    get_repository,
    get_sha,
    load_github_event,
)


def test_detect_github_context(monkeypatch, tmp_path):
    event_path = tmp_path / "event.json"
    event_path.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("GITHUB_EVENT_NAME", "issues")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))
    monkeypatch.setenv("GITHUB_REPOSITORY", "mdudaj/karakana")
    monkeypatch.setenv("GITHUB_REF_NAME", "main")
    monkeypatch.setenv("GITHUB_SHA", "abc123")
    monkeypatch.setenv("GITHUB_ACTOR", "octocat")

    context = detect_github_context()

    assert context["GITHUB_EVENT_NAME"] == "issues"
    assert get_event_path() == event_path
    assert get_repository() == "mdudaj/karakana"
    assert get_ref_name() == "main"
    assert get_sha() == "abc123"
    assert get_actor() == "octocat"


def test_load_github_event(monkeypatch, tmp_path):
    event_path = tmp_path / "event.json"
    event_path.write_text(json.dumps({"issue": {"title": "Test issue"}}), encoding="utf-8")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))

    event = load_github_event()

    assert event["issue"]["title"] == "Test issue"
