---
name: karakana-handoff
description: Use this skill to summarize current work into a compact handoff for another agent, Codex task, future session, or GitHub issue.
version: 0.1.0
risk_level: low
category: productivity
scope: bundled
status: stable
visibility: public
bucket: productivity
activation:
  keywords:
    - handoff
    - transfer
    - summarize current work
    - continue later
    - next agent
    - codex task
  required_files: []
  optional_tools:
    - git
allowed_tools:
  - read_file
  - grep
  - code_search
requires_approval_for: []
---
# Karakana Handoff Skill

## Purpose

Create compact, accurate handoffs that let another agent or future session continue without rediscovering context.

## When to use this skill

Use when pausing work, transferring work to another agent, preparing a Codex task, summarizing a long session, or creating a GitHub issue from current state.

## When not to use this skill

Do not use as a substitute for tests, code review, or formal release notes. Do not include secrets or raw credential material.

## Quick Reference

- Capture the current goal, what changed, what remains, and where evidence lives.
- Include commands already run and commands still needed.
- Recommend the next skill only when it clearly helps the next step.

## Core concepts

- Handoffs preserve decision context, not every line of chat.
- The next agent needs exact files, artifacts, commands, risks, and definition of done.
- Unverified claims should be marked as assumptions or risks.

## Standard workflow

1. Identify the active goal and latest user request.
2. Summarize completed work with file and artifact references.
3. Record current repository state, failing checks, and unresolved questions.
4. Recommend next actions and relevant Karakana skills.
5. State risks, constraints, and definition of done.

## Pitfalls

- Do not omit failed commands or partial work.
- Do not include secrets, tokens, `.env` content, or private credentials.
- Do not claim completion without evidence.

## Verification

- Check `git status` and relevant test output before finalizing.
- Confirm file paths and artifact paths exist.
- Ensure the handoff is short enough to be read quickly.

## Safety rules

- Redact secret-like values.
- Preserve human review gates.
- Do not tell the next agent to deploy, push to main, or bypass tests.

## Required checks

- Current goal is explicit.
- Relevant files and artifacts are listed.
- Suggested next actions are actionable.
- Risks and constraints are documented.
- Definition of done is testable.

## Output format

```markdown
# Handoff

## Current Goal

## What Was Done

## Current State

## Relevant Files and Artifacts

## Suggested Skills

## Suggested Next Actions

## Risks and Constraints

## Commands to Run

## Definition of Done
```

## Examples

- Summarize a partially implemented milestone with files changed, commands run, failing tests, and next skill recommendations.
- Convert a finished implementation session into a compact future-session handoff.
