---
name: github-pr-review
description: Use this skill for reviewing GitHub pull requests for correctness, security, maintainability, tests, migrations, deployment risk, documentation, and backwards compatibility.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - database_migration
  - authentication_change
  - permission_change
  - production_config_change
  - destructive_command
activation:
  keywords:
    - pull request
    - pr review
    - review
    - diff
  required_files:
    - AGENTS.md
  optional_tools:
    - git
    - pytest
category: development
scope: bundled
---
# GitHub PR Review

## Purpose

Guide serious, actionable review of GitHub pull requests.

## When to use this skill

Use when reviewing diffs for correctness, security, maintainability, tests, migrations, deployment risk, documentation, and backwards compatibility.

## When not to use this skill

Do not use for style-only commentary or broad planning without a concrete change to review.

## Core concepts

- Findings should be grounded in changed files and observable behavior.
- Prioritize blocking correctness, security, data loss, migration, and deployment risks.
- Missing tests matter when behavior changes.

## Standard workflow

1. Inspect the diff and affected ownership boundaries.
2. Identify behavior changes and risk areas.
3. Check tests and migration/deployment implications.
4. Report only actionable findings.
5. Include residual risk when verification is incomplete.

## Safety rules

- Do not approve risky changes without evidence.
- Do not ignore authentication, permission, secret, or data loss risks.
- Do not over-comment on style-only issues.

## Required checks

- Check changed tests or missing tests.
- Check security-sensitive code paths.
- Check migrations and deployment notes when applicable.

## Output format

Return blocking issues, non-blocking suggestions, test gaps, security risks, and deployment risks.

## Quick Reference

- Lead with correctness, security, data, migration, and deployment risks.
- Cite changed files and observable behavior.
- Treat missing tests as important when behavior changes.

## Pitfalls

- Do not bury blocking findings under style comments.
- Do not approve authentication, permission, migration, or production changes without evidence.
- Do not speculate when the diff or tests can be inspected.

## Verification

- Inspect the relevant diff and owning files.
- Run or request focused tests where practical.
- Report residual risk when verification is incomplete.

## Examples

- Flag a missing permission check in a changed API endpoint.
- Flag a migration that can lose data without a rollback plan.
