---
name: engineering-design-records
description: Author or revise Markdown ADRs and design descriptions that retain alternatives,
  stakeholder concerns, quality constraints and authoritative interface or diagram
  links.
version: 0.1.0
risk_level: medium
category: documentation
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
  - draft ADR
  - write architecture decision
  - document design views
  - design description
  - architecture decision record
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
# engineering-design-records

## Purpose

Record consequential decisions and relevant design views so later reviewers can assess context, trade-offs, consequences and actual decision authority.

## When to use this skill

Use for requested ADR/design authoring, revision or review. Use a compact record for a small choice; select views by affected stakeholder concerns.

## When not to use this skill

Use system-design-thinking for unresolved system reasoning, and existing domain/UX skills for their actual implementation constraints. Do not create a new decision process or replace a machine schema.

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

ADR decision status is separate from containing-document status. Proposed is not Accepted; accepted choices retain authority evidence and history. A design view addresses a concern; a diagram without context is insufficient.

Markdown is the primary documentation source. Preserve explicit authority for
native engine fields and machine schemas. Use namespace/type/ID separately from
revision; keep unknowns explicitly unconfirmed. Review and evidence apply to a
scoped revision, not automatically to changed content.

## Standard workflow

Inspect existing accepted decisions, affected sources, interfaces, stakeholder concerns and verification evidence. Reuse current design reasoning or surface the missing decision. Select the needed reference below. Record credible alternatives and consequences; keep the decision Proposed until actual scoped authority is evidenced. Preserve previous decisions on supersession and identify affected requirements/contracts.

Conditional guidance:

- For consequential options, decision or supersession, read [references/adr.md](references/adr.md).
- For stakeholder concerns, scenarios and architecture views, read [references/design-views.md](references/design-views.md).
- For interfaces, quality, data/security, operations or UX concerns, read [references/contracts-and-quality.md](references/contracts-and-quality.md).

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

Check alternatives/drivers, positive and negative consequences, authority/status, source revision and supersession. Check relevant behavior, UX look/feel, failure paths, security/data/operations and measured quality. Link authoritative schema/diagram sources with revision and limitations.

## Output format

Canonical Markdown ADR/design narrative and selected structured views. Include full rationale, source references, open questions, proposed status and requested review; a workbook may excerpt it only with complete-source links.

## Examples

Read [examples/design.md](examples/design.md) for a complete synthetic authored example.
Its namespace is `example`; facts, owners and verification gaps are illustrative,
not a real project draft or an approval.

An inquiry such as “do we have skills for a roadmap?” receives the skill name and
capability. “Draft a roadmap from these agreed outcomes” authorizes a project
copy, with assumptions and forecast limits recorded.

## Pitfalls

Do not backfill an Accepted decision from a successful build or an agreeable workbook cell. Do not replace retained reasoning with a short summary.

## Verification

Check source adequacy and observable acceptance with actual reviewers/evidence.
For structured sources, run P02 validation and an audience export when requested.
Run `karakana skill validate skills/engineering-design-records` and
`karakana eval run --skill engineering-design-records` for skill maintenance.
Deterministic evals check instruction coverage; they do not prove model behavior,
reviewer agreement, operational readiness or stable promotion.
