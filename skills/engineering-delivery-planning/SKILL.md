---
name: engineering-delivery-planning
description: Author or revise outcome roadmaps, milestones and bounded implementation
  plans in Markdown once delivery direction is selected.
version: 0.1.0
risk_level: medium
category: documentation
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
  - draft roadmap
  - write milestone plan
  - document implementation plan
  - delivery plan documentation
  required_files: []
  optional_tools:
  - python
  - pytest
allowed_tools:
- read_file
- grep
- code_search
- python
- run_tests
requires_approval_for:
- source_approval_change
- remote_publish
---
# engineering-delivery-planning

## Purpose

Record selected delivery direction as outcomes, checkpoints and executable instructions, keeping forecasts, dependencies and agreement evidence clear.

## When to use this skill

Use for requested roadmap/milestone/implementation-plan authoring, revision or review when direction is already known.

## When not to use this skill

Use next-milestone-decision when the question is what to do next. Do not execute the selected plan or invent estimates, owners or committed dates.

## Quick Reference

Preserve the request type. A skills inquiry returns catalogue information; do not
draft. Research returns evidence, planning returns a proposed plan. Draft/revise
only when requested or already authorized. Export the requested source/audience;
publishing requires its separate existing authorization.

Use the [shared content contract](../../docs/engineering-artifacts.md) and the
[generic blank template](../../docs/skills/engineering-artifact-catalogue/TEMPLATE.md)
when a structured export is needed. Instantiate applicable sections in a project
copy; the global template contains no project facts. Ordinary narrative review
need not create every table. Read only references relevant to the task.

## Core concepts

A roadmap describes outcomes and learning horizons. A milestone has observable output/acceptance. A task has evidence to inspect and checks to perform. Forecasts and commitments have different authority.

Markdown is the primary documentation source. Preserve explicit authority for
native engine fields and machine schemas. Use namespace/type/ID separately from
revision; keep unknowns explicitly unconfirmed. Review and evidence apply to a
scoped revision, not automatically to changed content.

## Standard workflow

Inspect selected direction, current baseline, requirements/backlog, dependencies, risks and prior delivery checks. Resolve contradicted assumptions from available sources; use the selection skill only if direction is materially open. Select the needed reference below. Draft outcome horizons and small demonstrable milestones, then bounded tasks with references, interfaces, ordered steps, checks and recovery. Review dependency/approval gaps without starting execution.

Conditional guidance:

- For strategy, outcome horizons or review triggers, read [references/roadmap.md](references/roadmap.md).
- For bounded outputs, checkpoints or agreements, read [references/milestones.md](references/milestones.md).
- For copy-ready task instructions and verification/recovery, read [references/implementation-plan.md](references/implementation-plan.md).

For an accompanying workbook, use engineering-workbooks and the
[P02 opt-in tool guide](../../docs/skills/engineering-artifact-catalogue/P02.md).
Reuse the project's existing lifecycle/artifact gates; do not create another
approval process or infer external permissions from this skill.

## Safety rules

Keep sources/project context isolated and redact sensitive information before
sharing. No live model calls, remote writes, deployment or source approval changes
follow from document drafting/export. Actual approvals require the project's
existing authority and scoped evidence. An unresolved material decision stays
visible; it cannot silently become an agreed fact.

## Required checks

Check outcome/measure, horizon/confidence, review trigger, dependency owners, estimate basis, agreed scope and evidence. Every task names what to inspect, governing references, steps, verification command/expected result and applicable recovery/approval.

## Output format

Canonical Markdown outcome roadmap and selected milestone/task records, explicitly proposed or evidenced agreed; list blockers, uncertainty and the next bounded action. No manufactured calendar commitments.

## Examples

Read [examples/plan.md](examples/plan.md) for a complete synthetic authored example.
Its namespace is `example`; facts, owners and verification gaps are illustrative,
not a real project draft or an approval.

An inquiry such as “do we have skills for a roadmap?” receives the skill name and
capability. “Draft a roadmap from these agreed outcomes” authorizes a project
copy, with assumptions and forecast limits recorded.

## Pitfalls

A dated feature list is not an outcome roadmap. An estimate is not an accepted milestone. Planning instructions do not authorize deployment or remote mutation.

## Verification

Check source adequacy and observable acceptance with actual reviewers/evidence.
For structured sources, run P02 validation and an audience export when requested.
Run `karakana skill validate skills/engineering-delivery-planning` and
`karakana eval run --skill engineering-delivery-planning` for skill maintenance.
Deterministic evals check instruction coverage; they do not prove model behavior,
reviewer agreement, operational readiness or stable promotion.
