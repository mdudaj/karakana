---
name: karakana-self-improvement
description: Use this skill when Karakana reflects on its own memory, skills, prompts, tests, workflows, evaluation cases, or reviewable improvement proposals.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
  - python
requires_approval_for:
  - skill_update
  - memory_update
  - prompt_update
  - eval_update
  - workflow_change
  - destructive_command
activation:
  keywords:
    - karakana
    - self-improvement
    - proposal
    - eval
  required_files:
    - KARAKANA.md
    - KARAKANA_AGENT_GUIDE.md
  optional_tools:
    - pytest
    - git
category: self-improvement
scope: bundled
status: stable
visibility: public
bucket: self-improvement
---
# Karakana Self Improvement

## Purpose

Guide reviewable improvement of Karakana memory, skills, prompts, tests, and workflows.

## When to use this skill

Use when reflecting on Karakana behavior, proposing memory updates, proposing skill updates, adding evals, improving prompts, or planning regression protection.

## When not to use this skill

Do not use for silent self-modification, production deployment, or unrelated application feature work.

## Core concepts

- Self-improvement must be visible, reviewable, testable, and reversible.
- Memory, skill, prompt, and eval changes should be proposed through patches or pull requests.
- Risky changes require human approval.

## Standard workflow

1. Review recent task evidence and current repository state.
2. Identify missing memory, weak skills, prompt gaps, or eval gaps.
3. Propose small changes with rationale and risk.
4. Add tests or eval cases where practical.
5. Require human review before merge.

## Safety rules

- Do not silently rewrite durable memory or skills.
- Do not bypass failing tests.
- Do not modify workflows or protected behavior without approval.

## Required checks

- Check `KARAKANA_AGENT_GUIDE.md`.
- Check affected memory, skill, prompt, and test files.
- Run relevant tests.

## Output format

Return proposed updates, rationale, risk level, tests, and review requirements.

## Examples

- Propose a new eval after a repeated review miss.
- Add a skill checklist after a recurring implementation pitfall.

## Quick Reference

- Keep self-improvement proposal-based and reviewable.
- Prefer memory, skill, prompt, eval, or documentation updates over source mutation.
- Add tests or evals for recurring misses.

## Pitfalls

- Do not treat reflection as permission to rewrite behavior silently.
- Do not apply high-risk changes without human review.
- Do not propose broad rewrites when a small eval or checklist would reduce risk.

## Verification

- Run `karakana skill validate-all`.
- Run `karakana eval run`.
- Run focused `pytest` tests for changed governance behavior.
