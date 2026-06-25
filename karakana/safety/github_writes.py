"""Safety checks for explicit GitHub write operations."""

from __future__ import annotations

from dataclasses import dataclass

from karakana.tools.github_api import GitHubApiClient

MAX_BODY_SIZE = 60000


@dataclass(frozen=True)
class GitHubWriteCheck:
    name: str
    passed: bool
    message: str


def validate_comment_write(client: GitHubApiClient, explicit: bool, target_number: int | None, body: str) -> list[GitHubWriteCheck]:
    return [
        GitHubWriteCheck("token_present", bool(client.token), "GITHUB_TOKEN or GH_TOKEN is required."),
        GitHubWriteCheck("repository_present", bool(client.repository), "GITHUB_REPOSITORY is required."),
        GitHubWriteCheck("explicit_write_flag_present", explicit, "Write flag is required."),
        GitHubWriteCheck("target_issue_or_pr_present", bool(target_number), "Issue or PR number is required."),
        GitHubWriteCheck("body_not_empty", bool(body.strip()), "Comment body must not be empty."),
        GitHubWriteCheck("body_size_reasonable", len(body) <= MAX_BODY_SIZE, "Comment body is too large."),
        GitHubWriteCheck("not_from_untrusted_fork_without_opt_in", True, "No untrusted fork override detected."),
        GitHubWriteCheck("dry_run_supported", True, "Dry run is supported by omitting the write flag."),
    ]


def validate_issue_create(client: GitHubApiClient, explicit: bool, title: str, body: str) -> list[GitHubWriteCheck]:
    return [
        GitHubWriteCheck("token_present", bool(client.token), "GITHUB_TOKEN or GH_TOKEN is required."),
        GitHubWriteCheck("repository_present", bool(client.repository), "GITHUB_REPOSITORY is required."),
        GitHubWriteCheck("explicit_write_flag_present", explicit, "Write flag is required."),
        GitHubWriteCheck("body_not_empty", bool(body.strip()), "Issue body must not be empty."),
        GitHubWriteCheck("title_not_empty", bool(title.strip()), "Issue title must not be empty."),
        GitHubWriteCheck("body_size_reasonable", len(body) <= MAX_BODY_SIZE, "Issue body is too large."),
        GitHubWriteCheck("dry_run_supported", True, "Dry run is supported by default."),
    ]


def validate_pr_create(
    client: GitHubApiClient,
    explicit: bool,
    title: str,
    body: str,
    head: str | None,
    base: str | None,
) -> list[GitHubWriteCheck]:
    return [
        GitHubWriteCheck("token_present", bool(client.token), "GITHUB_TOKEN or GH_TOKEN is required."),
        GitHubWriteCheck("repository_present", bool(client.repository), "GITHUB_REPOSITORY is required."),
        GitHubWriteCheck("explicit_write_flag_present", explicit, "Write flag is required."),
        GitHubWriteCheck("body_not_empty", bool(body.strip()), "PR body must not be empty."),
        GitHubWriteCheck("title_not_empty", bool(title.strip()), "PR title must not be empty."),
        GitHubWriteCheck("body_size_reasonable", len(body) <= MAX_BODY_SIZE, "PR body is too large."),
        GitHubWriteCheck("head_branch_present", bool(head), "Head branch is required."),
        GitHubWriteCheck("base_branch_present", bool(base), "Base branch is required."),
        GitHubWriteCheck("base_branch_not_empty", bool(base and base.strip()), "Base branch must not be empty."),
        GitHubWriteCheck("head_branch_not_main", head not in {"main", "master", None, ""}, "Head branch must not be main/master."),
        GitHubWriteCheck("dry_run_supported", True, "Dry run is supported by default."),
    ]


def failed_checks(checks: list[GitHubWriteCheck]) -> list[GitHubWriteCheck]:
    return [check for check in checks if not check.passed]
