---
name: engineering-requirements
description: Author or revise Markdown PRDs, requirements, user stories, acceptance
  criteria and traceability from resolved project intent and source evidence.
version: 0.1.0
risk_level: medium
category: documentation
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
  - draft requirements
  - write PRD
  - document user stories
  - acceptance criteria documentation
  - requirements traceability
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
# engineering-requirements

## Purpose

Turn resolved intent into reviewable requirements, stories and verification boundaries. Preserve an existing engine store when it owns native fields.

## When to use this skill

Use for requested authoring/revision of a PRD, specification, stories, criteria or requirements traceability; also for review of those artifacts.

## When not to use this skill

Use requirements-elicitation for material unresolved intent and grill-with-docs for a challenged plan. Do not decompose or generate engine issues merely to answer a skills inquiry.

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

Needs, solution choices and verification observations are different records. Requirement IDs are stable; text edits change revision, not identity. Proposed priority is distinct from agreed priority.

Markdown is the primary documentation source. Preserve explicit authority for
native engine fields and machine schemas. Use namespace/type/ID separately from
revision; keep unknowns explicitly unconfirmed. Review and evidence apply to a
scoped revision, not automatically to changed content.

## Standard workflow

Inspect the governing project instructions, current requirements/decisions, domain terms, source schemas and evidence. Reuse resolved elicitation; keep assumptions/open decisions explicit. Select the needed reference below. Draft the smallest useful set with source IDs and observable criteria. Link defined test cases separately from actual runs; review omissions, conflicts and changed approval applicability.

Conditional guidance:

- For PRD, needs, scope or requirement revision, read [references/requirements.md](references/requirements.md).
- For stories, acceptance criteria or test/UAT definitions, read [references/stories-and-acceptance.md](references/stories-and-acceptance.md).
- For links, changed baselines or native engine ownership, read [references/traceability.md](references/traceability.md).

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

Check scope/non-goals, need/rationale, domain terminology, stable IDs, criteria/verification method, typed links and unresolved acceptance decisions. Retain native PRD/story/issue IDs and engine-owned values; generated engine Markdown is not an editable master.

## Output format

Canonical Markdown with contract metadata when export is needed; substantive context/scope/requirements, selected stories/criteria and traceability, evidence limits and requested review. Separate draft content from implementation tasks and actual test results.

## Examples

Read [examples/requirements.md](examples/requirements.md) for a complete synthetic authored example.
Its namespace is `example`; facts, owners and verification gaps are illustrative,
not a real project draft or an approval.

An inquiry such as “do we have skills for a roadmap?” receives the skill name and
capability. “Draft a roadmap from these agreed outcomes” authorizes a project
copy, with assumptions and forecast limits recorded.

## Pitfalls

A story sentence is a discussion aid, not a complete specification. A defined acceptance case is not a passed test. Do not guess priority from ID prefixes.

## Verification

Check source adequacy and observable acceptance with actual reviewers/evidence.
For structured sources, run P02 validation and an audience export when requested.
Run `karakana skill validate skills/engineering-requirements` and
`karakana eval run --skill engineering-requirements` for skill maintenance.
Deterministic evals check instruction coverage; they do not prove model behavior,
reviewer agreement, operational readiness or stable promotion.
