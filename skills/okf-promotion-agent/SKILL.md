---
name: okf-promotion-agent
description: Use this skill when reviewing artifacts for promotion into Karakana OKF concepts, proposing concept drafts, or making OKF the entry point for agent workflow context.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
  - grep
  - code_search
  - pytest
requires_approval_for:
  - okf_concept_promotion
  - cross_project_knowledge_promotion
  - workflow_change
  - safety_policy_change
activation:
  keywords:
    - OKF
    - promotion
    - promote artifact
    - concept
    - knowledge graph
category: self-improvement
scope: bundled
status: experimental
visibility: public
bucket: self-improvement
---
# OKF Promotion Agent

## Quick Reference

- Start from OKF concepts before raw source inspection.
- Promote only stable, durable knowledge.
- Generate promotion proposals first; do not write directly into `okf/` by default.
- Record source artifact, reason, reviewer, date, verification, and relationships.
- Reject blocked paths, secrets, and cross-project promotion without metadata.

## Purpose

Curate durable Karakana and project knowledge into OKF concepts through a systematic, reviewable, proposal-first workflow.

## When to use this skill

Use when a task asks to promote artifacts into OKF, review OKF context, create concept proposals, add project knowledge to the OKF graph, or make an agent workflow start from curated concepts.

## When not to use this skill

Do not use for raw log archiving, one-off notes, failed experiments, or unreviewed bulk migration of `.karakana/` runtime artifacts.

## Core concepts

- OKF concepts are durable knowledge, not runtime evidence.
- Runtime artifacts can justify concepts, but they are not concepts until explicitly promoted.
- Promotion is proposal-first and reviewable.
- Source artifacts stay authoritative; concepts summarize and link.
- Project boundaries are part of safety.

## Standard workflow

1. Validate current OKF concepts.
2. Select relevant OKF context for the project/task.
3. Scan candidate artifacts.
4. Classify each artifact as eligible or ineligible with a reason.
5. Draft concept and promotion record proposals for eligible artifacts only.
6. Validate the proposed concept frontmatter.
7. Ask for review before applying a proposal into `okf/`.
8. Refresh the handoff with loaded and changed concept IDs.

## Promotion matrix

- Accepted ADR: eligible as `ADR`.
- Ready PRD or user stories: eligible as `Requirement` or `UserStory`.
- Schema file: eligible as `Schema`.
- Stable design-system rule: eligible as `DesignSystemRule`.
- Safety or model-routing decision: eligible as `SafetyRule` or `ModelRoute`.
- Verified recurring lesson: eligible as `Lesson`.
- Stable handoff decision or exact next action: eligible as `Handoff`.
- Raw trace, noisy log, failed experiment, temporary note: ineligible by default.
- Blocked or secret-bearing source: ineligible.
- Cross-project promotion without explicit metadata: ineligible.

## Safety rules

- Do not auto-promote.
- Do not bulk-promote runtime artifacts.
- Do not read or reference `.env`, `.env.*`, `secrets/**`, private keys, tokens, or credential-bearing URLs.
- Do not promote project-specific concepts into another project without explicit crosslink metadata.
- Do not bypass workflow, model, patch, safety, or GitHub approval gates.

## Required checks

- Is this artifact durable knowledge or runtime evidence?
- Is the source path safe?
- Which project owns the concept?
- Which concept type is correct?
- What source artifact remains authoritative?
- What verification proves the promotion is safe?
- Which relationships should link the concept into the graph?
- Has the proposal been reviewed before applying?

## Output format

```markdown
## OKF Promotion Review

- Source artifact:
- Eligibility:
- Suggested concept ID:
- Suggested type:
- Project:
- Reason:
- Required review:
- Verification:
- Relationships:
```

## Examples

- Promote `docs/adr/0003-okf-entry-point-and-promotion-agent.md` as an `ADR` concept proposal.
- Promote `schemas/curriculum/source_registry.schema.json` as a project `Schema` concept proposal.
- Reject `.karakana/traces/...` as runtime evidence unless a stable lesson is extracted first.

## Pitfalls

- Copying full source documents into concepts instead of linking them.
- Treating a handoff as durable just because it is recent.
- Mixing one project's concept into another project's OKF bundle.
- Letting promotion proposals skip review because validation passed.

## Verification

- `karakana okf validate --strict`
- `karakana okf scan-promotions`
- `karakana skill validate-all`
- Focused tests for promotion scanning and proposal generation.
