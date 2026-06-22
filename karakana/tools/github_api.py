"""Small GitHub REST API client for explicit opt-in writes."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass(frozen=True)
class GitHubApiError(Exception):
    message: str
    status: int | None = None

    def __str__(self) -> str:
        return f"{self.message}" + (f" (status {self.status})" if self.status else "")


class GitHubApiClient:
    def __init__(
        self,
        token: str | None = None,
        repository: str | None = None,
        api_url: str | None = None,
    ):
        self.token = token if token is not None else os.environ.get("GITHUB_TOKEN")
        self.repository = repository if repository is not None else os.environ.get("GITHUB_REPOSITORY")
        self.api_url = (api_url or os.environ.get("GITHUB_API_URL") or "https://api.github.com").rstrip("/")

    def is_configured(self) -> bool:
        return bool(self.token and self.repository)

    def post_issue_comment(self, issue_number: int, body: str) -> dict:
        return self._request("POST", f"/repos/{self.repository}/issues/{issue_number}/comments", {"body": body})

    def create_issue(self, title: str, body: str, labels: list[str] | None = None) -> dict:
        payload = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        return self._request("POST", f"/repos/{self.repository}/issues", payload)

    def create_pull_request(self, title: str, body: str, head: str, base: str, draft: bool = True) -> dict:
        return self._request(
            "POST",
            f"/repos/{self.repository}/pulls",
            {"title": title, "body": body, "head": head, "base": base, "draft": draft},
        )

    def _request(self, method: str, path: str, payload: dict) -> dict:
        if not self.token:
            raise GitHubApiError("GITHUB_TOKEN is required for GitHub write operations")
        if not self.repository:
            raise GitHubApiError("GITHUB_REPOSITORY is required for GitHub write operations")
        request = urllib.request.Request(
            self.api_url + path,
            data=json.dumps(payload).encode("utf-8"),
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "karakana",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8")
            raise GitHubApiError(f"GitHub API request failed: {error_body}", exc.code) from exc
        if not body:
            return {}
        return json.loads(body)
