---
name: write-karakana-skill
description: Use this skill when creating, revising, validating, or promoting Karakana skills.
version: 0.1.0
risk_level: medium
category: self-improvement
scope: bundled
status: stable
visibility: public
bucket: self-improvement
activation:
  keywords:
    - write skill
    - create skill
    - new skill
    - update skill
    - skill validation
    - skill eval
    - skill promotion
  required_files:
    - skills
  optional_tools:
    - pytest
    - git
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
  - python
requires_approval_for:
  - skill_promotion
  - high_risk_tool_permission
---
# Write Karakana Skill

## Purpose

Guide creation, revision, validation, and promotion of focused Karakana skills.

## When to use this skill

Use when adding a new skill, updating an existing skill, adding skill evals, validating metadata, or promoting a skill through the lifecycle.

## When not to use this skill

Do not create a new skill when an existing skill can be safely extended. Do not use skills for deterministic operations that need a tool.

## Quick Reference

- Keep skills small, focused, and reviewable.
- Add evals for non-trivial or high-risk skills.
- Validate with `karakana skill validate <skill-dir>` and `karakana skill validate-all`.
- Update the skill index with `karakana skill index --write` when metadata changes are ready.

## Core concepts

- Skills describe workflows and judgment; tools execute narrow deterministic operations.
- New skills need valid metadata, activation guidance, examples, safety rules, output format, and verification steps.
- Lifecycle metadata communicates maturity without making experimental work invisible.
- Index metadata includes `status`, `visibility`, `bucket`, `description`, and the skill `path`.
- `visibility: hidden` skills are excluded from public indexes.
- `status: deprecated` skills remain reviewable but should warn users and name replacements when available.

## Standard workflow

1. Check whether an existing skill can be extended.
2. Define the skill purpose, activation signals, scope, risk level, and allowed tools.
3. Write `SKILL.md` with required and recommended sections.
4. Add realistic examples and eval cases for non-trivial behavior.
5. Validate the skill and run relevant evals/tests.
6. Update documentation and index entries when ready.

## Pitfalls

- Do not create broad catch-all skills.
- Do not grant high-risk tool permissions without explicit approval requirements.
- Do not promote a skill to stable before it has verification evidence.

## Verification

- `karakana skill validate skills/<skill-name>`
- `karakana skill validate-all`
- `karakana eval run --skill <skill-name>` for non-trivial skills.
- `pytest` when parser, validator, or CLI behavior changes.

## Safety rules

- Do not include secrets in examples.
- Do not add live model or GitHub write behavior through a skill.
- High-risk domains require explicit approval requirements and safety checks.

## Required checks

- `SKILL.md` exists.
- Metadata is valid.
- Activation guidance is present when useful.
- Quick Reference, Core concepts, Pitfalls, Verification, Examples, Safety rules, and Output format are present.
- Non-trivial skills have eval cases.
- Documentation or index updates are included when appropriate.

## Output format

Return a skill creation or revision plan with:

- target skill path,
- metadata,
- required sections,
- eval cases,
- validation commands,
- risks,
- review requirements.

## Examples

- Create a domain skill for a recurring workflow pattern with examples, pitfalls, and evals.
- Revise an experimental skill after eval failures, then keep it experimental until human review.
