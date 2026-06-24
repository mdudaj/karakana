# ADR 0001: Require Delivery Artifact Gate for Karakana Harness Work

Date: 2026-06-20

## Status

Accepted

## Context

Karakana-managed work has been accumulating repeated chat-level instructions about requirements, UX, ADRs, stories, milestones, tests, and handoffs. Chat instructions are easy to lose across sessions and do not reliably guide future implementation or self-improvement.

The harness needs a systematic way to decide which durable artifacts must guide each implementation slice before code changes begin, across Karakana itself and managed projects such as `msc-platform`.

## Decision

Add a `delivery-artifact-gate` skill and make it available as a general Karakana harness skill. Require it in the `karakana` and `msc-platform` skillpacks.

The skill requires agents to classify the work, select the smallest relevant artifact set, create or update missing artifacts before implementation, add verification coverage, and refresh the handoff.

The gate is also a delivery blocker: non-trivial work must not be marked done, merged, or handed off as complete until every required artifact exists or the delivery notes explicitly record why a normally expected artifact is not applicable. Code, tests, and a PR are not sufficient when requirement, ADR, milestone, schema, UX, verification, or handoff artifacts are required by the work type.

## Consequences

- Non-trivial work should no longer proceed directly from chat request to code.
- UI changes should produce or update UX grill/research artifacts before implementation.
- Durable architecture or ID-generation decisions should produce ADRs.
- User-visible features should produce user stories or acceptance criteria.
- Schema/data/evidence changes should update schemas, examples, and validation.
- Handoffs should record both implementation and the artifacts that justified it.
- Delivery reviews should check artifact readiness before accepting a slice as complete.
- Rework caused by missing requirements, ADRs, milestone instructions, delivery instructions, UX requirements, schemas, tests, or handoffs should be treated as a process failure to correct before the next slice proceeds.

## Verification

- `karakana skill validate-all`
- `karakana skillpack validate-all`
- Focused project tests/evals for the changed scope
