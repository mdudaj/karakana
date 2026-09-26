---
name: engineering-workbooks
description: Export canonical engineering documents as audience Excel views and report
  returned-workbook feedback against an immutable source baseline using local Karakana
  tools.
version: 0.1.0
risk_level: medium
category: documentation
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
  - engineering workbook
  - audience Excel export
  - engineering artifact spreadsheet
  - workbook feedback
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
# engineering-workbooks

## Purpose

Share engineering documentation as a derived audience view and preserve review input while Markdown and declared native sources retain authority.

## When to use this skill

Use for requested engineering artifact Excel exports, baseline checks or returned-workbook feedback reports.

## When not to use this skill

Do not use for unrelated financial/data-analysis models or general Excel editing. Do not author a second master, apply feedback automatically or publish to remote services.

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

Markdown is primary; native engine fields remain Engine JSON-owned. XLSX is a derived view; JSON is its generated baseline snapshot. Qualified IDs join rows; row numbers and hashes are not identity. Review feedback is proposed input.

Markdown is the primary documentation source. Preserve explicit authority for
native engine fields and machine schemas. Use namespace/type/ID separately from
revision; keep unknowns explicitly unconfirmed. Review and evidence apply to a
scoped revision, not automatically to changed content.

## Standard workflow

Inspect the canonical sources, contract metadata, native authority/binding registry, requested audience and output root. Select the needed reference below. Use the existing opt-in module CLI to validate and export new XLSX/JSON pairs; check omissions and blockers. Preserve original baselines and annotations. Compare returned workbooks against baseline and current sources, then report conflicts for the governing source review workflow.

Conditional guidance:

- For source validation, new export, immutable baseline or feedback report, read [references/workbook-contract.md](references/workbook-contract.md).
- For audience selection, omissions, readability or office checks, read [references/audience-profiles.md](references/audience-profiles.md).

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

Check all source hashes/revisions, audience/profile, immutable workbook/snapshot identity and complete-source links. Check stale/conflicting input, comments/formulas, added/deleted identities and unsupported sheets. Inspect useful wrapping/navigation and office rendering; state native Excel/accessibility checks actually performed.

## Output format

New audience XLSX plus JSON baseline, or a new JSON proposed-feedback report. Include canonical source paths/namespace, audience, known limits, current validation issues and verification performed. Never resave the annotated input.

## Examples

Use the [synthetic source examples](../../docs/skills/engineering-artifact-catalogue/examples/feature.md)
and the reference CLI recipes to export a new profile and compare an annotated
copy. Never populate or replace the global blank workbook.

An inquiry such as “do we have skills for a roadmap?” receives the skill name and
capability. “Draft a roadmap from these agreed outcomes” authorizes a project
copy, with assumptions and forecast limits recorded.

## Pitfalls

Do not overwrite annotated exports or import workbook agreement as source approval. Relative source hyperlinks need the accompanying source files. Structural validation is not substantive acceptance.

## Verification

Check source adequacy and observable acceptance with actual reviewers/evidence.
For structured sources, run P02 validation and an audience export when requested.
Run `karakana skill validate skills/engineering-workbooks` and
`karakana eval run --skill engineering-workbooks` for skill maintenance.
Deterministic evals check instruction coverage; they do not prove model behavior,
reviewer agreement, operational readiness or stable promotion.
