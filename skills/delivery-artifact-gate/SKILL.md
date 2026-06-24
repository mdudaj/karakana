---
name: delivery-artifact-gate
description: Use this skill before implementing, revising, or reviewing project work when the work should be guided by durable artifacts such as requirements, ADRs, user stories, milestones, UX grill notes, schemas, examples, tests, or handoffs.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - pytest
requires_approval_for:
  - artifact_contract_change
  - schema_contract_change
  - evaluation_protocol_change
  - safety_policy_change
  - remote_push
activation:
  keywords:
    - deliver
    - implement
    - revise
    - requirements
    - ADR
    - user stories
    - milestone
    - UX
    - artifact
category: productivity
scope: bundled
status: experimental
visibility: public
bucket: productivity
---
# Delivery Artifact Gate

## Quick Reference

- Decide the required artifact set before code.
- Create missing requirements, UX, ADR, story, milestone, schema/example, readiness, or dogfood artifacts first.
- Treat missing required artifacts as a delivery blocker unless explicitly marked not applicable with rationale.
- Implement only artifact-backed scope.
- Add regression tests for durable rules.
- End with a refreshed handoff.

## Purpose

Ensure project work is guided by the right durable artifacts before implementation and leaves behind enough evidence for review, repeatability, and self-improvement.

## When to use this skill

Use before any non-trivial implementation, UI change, workflow change, schema/data change, research-platform change, or revision that reflects a new rule. Use it when a user says "deliver", "implement", "revise", "next", "requirements", "ADR", "stories", "milestone", "UX", or asks for a process improvement.

## When not to use this skill

Do not block tiny mechanical fixes when the artifact cost would exceed the change and no durable decision is being made. Still record verification in the handoff.

## Core concepts

- Chat instructions are not enough for durable project memory.
- The artifact set should be chosen before implementation begins.
- Artifacts guide scope; tests and handoffs prove what was delivered.
- Use the smallest artifact set that prevents repeated instructions and preserves implementation rationale.

## Core Rule

No meaningful implementation should start until the implementation-guiding artifact set is known. If a required artifact is missing, create or update it first, then implement against it.

No non-trivial delivery is complete until every required artifact exists or the PR, handoff, or delivery note records why the artifact is not applicable. Passing tests and merged code do not override missing requirements, ADR, milestone, delivery, UX, schema/example, verification, or handoff artifacts.

## Artifact Decision Matrix

Create or update the smallest relevant set:

- **Requirements grill**: ambiguous user intent, acceptance behavior, scope boundaries, or stakeholder expectations.
- **UX grill/research note**: navigation, page layout, forms, Material/Viewflow/Kisomo patterns, accessibility, or user workflow clarity.
- **ADR**: durable architecture, route organization, ID generation, schema ownership, workflow boundaries, or hard-to-reverse design decisions.
- **User stories**: user-visible capability with role, goal, acceptance criteria, and tests.
- **Milestone**: multi-step delivery, dependency sequencing, or a new bounded implementation slice.
- **Schema/example artifact**: data contracts, evidence manifests, imports/exports, generated IDs, evaluation records, or reproducibility outputs.
- **Implementation readiness note**: when requirements exist but the code change needs a scoped execution checklist.
- **Delivery readiness note**: when accepting a slice, list reused artifacts, new or updated artifacts, not-applicable artifacts, verification, residual gaps, and exact next action.
- **Dogfood/review artifact**: when using the project against itself, validating workflow ergonomics, or capturing self-improvement findings.
- **Tests/evals**: every behavior, access, schema, safety, and UX rule that can regress.
- **Handoff**: always at end of task in Karakana-managed projects.

## Standard workflow

1. Load the current project handoff and inspect required project docs.
2. Restate the work request as a bounded outcome.
3. Classify the change: UI/UX, data/schema, workflow, architecture, research/evaluation, safety, docs-only, or bug fix.
4. Select the artifact set from the matrix.
5. Check whether current artifacts already cover the change.
6. Create or update missing artifacts before code changes.
7. Implement only the artifact-backed scope.
8. Add or update tests/evals for the artifact rules.
9. Run focused verification.
10. Before marking delivery done, check that required artifacts exist or are explicitly not applicable.
11. Refresh the handoff with changed artifacts, verification, risks, and exact next action.

## Safety rules

- Do not weaken approval, secret, deployment, data, privacy, or production gates while creating artifacts.
- Treat schema, evaluation, safety, and participant-data artifacts as contract changes.
- Do not use artifact generation to justify scope expansion beyond the user request.
- Keep live model calls, GitHub writes, deploys, and remote pushes explicit opt-in.

## Required checks

- Which durable artifact tells us what to build?
- Which artifact records why this approach is correct?
- Which user story or acceptance criterion proves the work is done?
- Which tests/evals protect the rule from regression?
- Which handoff entry will let the next agent continue without repeating instructions?
- Is this implementation going beyond the artifact-backed scope?
- Are any required artifacts missing, renamed, or only implied by chat?
- If an expected artifact is not applicable, where is that rationale recorded?

## Output format

When planning, return:

```markdown
## Artifact Gate

- Work type:
- Required artifacts:
- Existing artifacts reused:
- New/updated artifacts:
- Implementation boundary:
- Verification required:
```

When implementing, include this gate in the working notes or artifact, then proceed.

## Examples

- UI revision: create/update UX grill, user stories, acceptance tests, and handoff.
- Generated ID rule: create/update ADR, requirements note, tests, and schema/example if persisted.
- Research evidence export: create/update schema, example fixture, PRD/story, validation command, and handoff.
- Small bug fix: reuse existing requirement, add focused regression test, and refresh handoff.

## Pitfalls

- Treating chat instructions as the only source of truth.
- Treating a passing test suite as proof that requirements and evidence artifacts were complete.
- Implementing UI before UX/navigation rules are written.
- Creating ADRs for trivial details while missing important user-story acceptance criteria.
- Updating code without updating schemas/examples.
- Ending with a handoff that lists code but not the artifacts that justified it.

## Verification

- `karakana skill validate-all`
- `karakana skillpack validate-all`
- Relevant project tests/evals for the changed scope.
