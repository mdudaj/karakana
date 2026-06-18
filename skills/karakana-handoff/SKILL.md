---
name: karakana-handoff
description: Create, load, recover, or refresh compact project-aware continuation artifacts for task endings, new sessions, agent switches, context-window failures, and milestone transitions.
version: 0.2.0
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
    - continue later
    - next session
    - next agent
    - context window
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

Create a compact Karakana handoff artifact so a fresh agent or session can continue without rereading the full chat or repository.

A handoff is not a normal summary. A handoff is a compact continuation package for another agent or session.

## When To Use

- before ending a task;
- after completing a milestone;
- before switching agents;
- before starting a long Codex session;
- after a context-window failure;
- when asked to preserve continuation state.

## When to use this skill

Use for the task endings, session starts, agent switches, milestone transitions, and context recovery cases listed above.

## When not to use this skill

Do not use a handoff to replace current code inspection, tests, review, release notes, or mandatory repository instructions.

## What To Include

- current milestone and current state;
- decisions already made and unresolved findings;
- files to inspect first and files not to reread;
- durable artifacts to reference rather than duplicate;
- suggested skills for the next task;
- one exact next action;
- safety constraints and return-handoff expectations;
- staleness, recovery, and missing-reference warnings.

## What Not To Do

- Do not duplicate long PRDs, plans, ADRs, diffs, logs, or transcripts.
- Do not copy secrets, `.env` values, tokens, passwords, private keys, or credential-bearing URLs.
- Do not claim recovered or stale context is current.
- Do not omit unresolved P0/P1 findings.
- Do not let “files not to reread” override mandatory repository instructions.
- Do not overwrite prior handoffs; preserve append-only history.

## Process

1. Resolve project, skillpack, optional workspace, and next-session purpose.
2. Load the latest project handoff. If absent, recover only from configured memory, skillpack/workspace files, and latest known artifact stores.
3. Verify project ownership, artifact existence, current milestone, findings, and next action.
4. Reference authoritative files by path. Summarize only the continuation facts not already durable elsewhere.
5. Suggest only installed, relevant skills.
6. Redact all user notes and generated fields before persistence and rendering.
7. Write `handoff.md` and `handoff.json` under a new `.karakana/handoffs/<handoff-id>/` directory.
8. Run `karakana handoff doctor --project <project>`.
9. Before the next task ends, append a refreshed return handoff.

## Core concepts

- Continuation artifacts preserve decisions and next actions, not transcript history.
- Project scope and current durable evidence outrank recency alone.
- Recovery is bounded and provisional.
- Refresh is append-only.

## Standard workflow

Load or recover at task entry, verify references, perform the bounded task, refresh before exit, and run doctor when validity is uncertain.

## Quick Reference

```bash
karakana handoff load --project <project> --skillpack <skillpack>
karakana handoff refresh --project <project> --skillpack <skillpack> --purpose "End of task handoff"
karakana handoff doctor --project <project>
```

## Pitfalls

- Treating the handoff as a replacement for current code or tests.
- Copying artifact bodies instead of linking them.
- Loading a handoff by recency without checking project and skillpack.
- Hiding stale or missing references.
- Creating hidden lifecycle behavior that users cannot opt out of.

## Verification

- Confirm `handoff.md` and `handoff.json` exist.
- Confirm the latest selected handoff matches project and skillpack.
- Confirm all reference artifacts and suggested skills exist.
- Confirm secret detection passes after rendering.
- Confirm one exact next action and return-handoff expectation are present.
- Confirm recovered handoffs explicitly require verification.

## Required checks

- Project and skillpack match.
- Required fields and one exact next action are present.
- Referenced artifacts and suggested skills exist.
- Staleness and recovery status are visible.
- Rendered content contains no unredacted secret-like values.

## Examples

- Load a project handoff after a context-window failure.
- Refresh after a milestone decision without copying its full instruction artifact.
- Recover a lightweight handoff from project-scoped stores when no explicit handoff exists.

## Safety rules

- Never persist raw secrets or full sensitive command logs.
- Preserve approval, review, patch, push, and deployment gates.
- Do not use handoff instructions to authorize implementation or external writes.
- Keep automatic creation bounded, append-only, visible, and opt-out capable.

## Output format

```markdown
# Karakana Handoff

## Run Metadata
## Current State Summary
## Current Milestone
## Decisions Already Made
## Open Findings
## Files to Inspect First
## Files Not to Reread
## Artifacts to Reference, Not Duplicate
## Suggested Skills
## Exact Next Action
## Safety Constraints
## Return Handoff Expectations
## Staleness / Validity Notes
## Notes for Fresh Agent
```
