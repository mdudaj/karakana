from karakana.safety.github_writes import failed_checks, validate_comment_write, validate_pr_create
from karakana.tools.github_api import GitHubApiClient


def test_comment_write_requires_explicit_flag():
    client = GitHubApiClient(token="token", repository="owner/repo")

    checks = validate_comment_write(client, explicit=False, target_number=1, body="body")

    assert any(check.name == "explicit_write_flag_present" for check in failed_checks(checks))


def test_comment_write_requires_token_and_repository():
    checks = validate_comment_write(GitHubApiClient(token="", repository=""), True, 1, "body")

    failed = {check.name for check in failed_checks(checks)}
    assert "token_present" in failed
    assert "repository_present" in failed


def test_pr_create_rejects_main_head():
    client = GitHubApiClient(token="token", repository="owner/repo")

    checks = validate_pr_create(client, True, "title", "body", "main", "main")

    assert any(check.name == "head_branch_not_main" for check in failed_checks(checks))
