---
name: ci-failure-analysis
description: Use this skill for failed GitHub Actions or CI logs, including log reduction, failure classification, root cause analysis, affected files, suggested patches, rerun guidance, and missing dependency detection.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - production_config_change
  - destructive_command
activation:
  keywords:
    - ci failure
    - github actions
    - test failure
    - build failure
  required_files:
    - pyproject.toml
  optional_tools:
    - pytest
    - git
category: development
scope: bundled
---
# CI Failure Analysis

## Purpose

Guide diagnosis of failed CI runs and test logs.

## When to use this skill

Use for GitHub Actions failures, test logs, dependency failures, lint failures, build failures, flaky tests, and rerun decisions.

## When not to use this skill

Do not use for unrelated feature planning or broad code review when no CI failure is present.

## Core concepts

- Reduce noisy logs to the first meaningful failure.
- Classify failures before patching.
- Distinguish product bugs from environment, dependency, and flaky failures.

## Standard workflow

1. Identify failing job and command.
2. Extract the first meaningful error.
3. Map the error to likely files and recent changes.
4. Suggest or apply a minimal patch.
5. Rerun focused tests or explain rerun guidance.

## Safety rules

- Do not bypass failing tests.
- Do not hide failures by weakening checks without justification.
- Do not change production config to satisfy CI without approval.

## Required checks

- Confirm the failing command.
- Check dependency or missing package errors.
- Run the narrowest local reproduction where possible.

## Output format

Return failure class, root cause, affected files, suggested fix, and rerun guidance.

## Examples

- Diagnose a failing pytest job from the first meaningful traceback.
- Separate flaky infrastructure failures from deterministic regressions.

## Quick Reference

- Find the first meaningful failure before editing.
- Classify dependency, environment, test, lint, build, and product failures separately.
- Prefer narrow reruns over broad retries.

## Pitfalls

- Do not hide failures by weakening checks.
- Do not change production configuration to satisfy CI without approval.
- Do not chase secondary errors before the root failure is understood.

## Verification

- Re-run the narrow failing command when possible.
- Run affected tests after a fix.
- Document skipped verification and rerun guidance.

- Diagnose a missing dependency from an import error.
- Identify a test failure caused by changed validation behavior.
