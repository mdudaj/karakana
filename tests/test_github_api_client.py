import json
import urllib.error

import pytest

from karakana.tools.github_api import GitHubApiClient, GitHubApiError


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.body


def test_client_configuration_from_env(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")

    client = GitHubApiClient()

    assert client.is_configured()


def test_client_configuration_accepts_gh_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GH_TOKEN", "token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")

    client = GitHubApiClient()

    assert client.is_configured()


def test_missing_token_behavior(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    client = GitHubApiClient(token=None, repository="owner/repo")

    with pytest.raises(GitHubApiError, match="GITHUB_TOKEN or GH_TOKEN"):
        client.create_issue("title", "body")


def test_post_issue_comment_request(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["auth"] = request.headers["Authorization"]
        return FakeResponse(b'{"html_url": "https://example/comment"}')

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = GitHubApiClient(token="token", repository="owner/repo", api_url="https://api.test")

    result = client.post_issue_comment(3, "body")

    assert captured["url"] == "https://api.test/repos/owner/repo/issues/3/comments"
    assert captured["body"] == {"body": "body"}
    assert captured["auth"] == "Bearer token"
    assert result["html_url"] == "https://example/comment"


def test_create_issue_request(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse(b'{"html_url": "https://example/issue"}')

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    GitHubApiClient(token="token", repository="owner/repo", api_url="https://api.test").create_issue(
        "title", "body", ["label"]
    )

    assert captured["url"] == "https://api.test/repos/owner/repo/issues"
    assert captured["body"] == {"title": "title", "body": "body", "labels": ["label"]}


def test_create_pr_request(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse(b'{"html_url": "https://example/pr"}')

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    GitHubApiClient(token="token", repository="owner/repo", api_url="https://api.test").create_pull_request(
        "title", "body", "head", "main", draft=True
    )

    assert captured["url"] == "https://api.test/repos/owner/repo/pulls"
    assert captured["body"]["draft"] is True
