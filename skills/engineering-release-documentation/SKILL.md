---
name: engineering-release-documentation
description: Author or revise Markdown release plans, evidence-backed release notes
  and adoption or handover guidance, separating planned scope from actual release
  and operational facts.
version: 0.1.0
risk_level: medium
category: documentation
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
  - draft release plan
  - write release notes
  - release documentation
  - adoption guide
  - release handover
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
# engineering-release-documentation

## Purpose

Help reviewers and users understand a release candidate, delivered changes and safe adoption from actual source/evidence, without manufacturing readiness.

## When to use this skill

Use for requested release-plan/notes/adoption/handover authoring, revision or review. Tailor to candidate, audience and the project release process.

## When not to use this skill

Do not publish, tag, deploy, activate users or claim operational acceptance from drafting. Existing release checks, runbooks and Karakana handoffs retain their authority.

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

Candidate verification, merge, publication, deployment and acceptance are separate facts. Release plans hold intended scope; release notes describe evidence-backed delivered changes. Defined tests differ from executed runs.

Markdown is the primary documentation source. Preserve explicit authority for
native engine fields and machine schemas. Use namespace/type/ID separately from
revision; keep unknowns explicitly unconfirmed. Review and evidence apply to a
scoped revision, not automatically to changed content.

## Standard workflow

Inspect the project version scheme, candidate/baseline, accepted scope, actual changes, checks/reviews, known gaps and runbooks. Select the needed reference below. Draft a plan with unverified gates explicit; write a delivered note only when its scoped observation exists. Separate user guidance from operator recovery and record tested revision/limits. Review audience usefulness and remaining adoption blockers.

Conditional guidance:

- For candidate scope, assurance, rollout and recovery planning, read [references/release-plan.md](references/release-plan.md).
- For delivered change communication or changelog, read [references/release-notes.md](references/release-notes.md).
- For user guidance, support, runbooks and continuation, read [references/adoption-and-handover.md](references/adoption-and-handover.md).

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

Check version/candidate/target, planned versus delivered scope, user impact, compatibility/migration, known limitations, evidence, recovery and support. Preserve Not run, Blocked, Skipped, Fail and Pass; absence is not success. Date forecasts as forecasts, actual events only from actual observations.

## Output format

Canonical Markdown release plan, selected notes and/or guidance with source IDs, evidence and gaps. Report implemented, verified, merged, published, deployed and accepted separately; unconfirmed facts remain explicit.

## Examples

Read [examples/release.md](examples/release.md) for a complete synthetic authored example.
Its namespace is `example`; facts, owners and verification gaps are illustrative,
not a real project draft or an approval.

An inquiry such as “do we have skills for a roadmap?” receives the skill name and
capability. “Draft a roadmap from these agreed outcomes” authorizes a project
copy, with assumptions and forecast limits recorded.

## Pitfalls

A passing test does not show publication, deployment or user acceptance. A commit list is not useful release communication; a forecast must not become a delivered change.

## Verification

Check source adequacy and observable acceptance with actual reviewers/evidence.
For structured sources, run P02 validation and an audience export when requested.
Run `karakana skill validate skills/engineering-release-documentation` and
`karakana eval run --skill engineering-release-documentation` for skill maintenance.
Deterministic evals check instruction coverage; they do not prove model behavior,
reviewer agreement, operational readiness or stable promotion.
