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

## Consequences

- Non-trivial work should no longer proceed directly from chat request to code.
- UI changes should produce or update UX grill/research artifacts before implementation.
- Durable architecture or ID-generation decisions should produce ADRs.
- User-visible features should produce user stories or acceptance criteria.
- Schema/data/evidence changes should update schemas, examples, and validation.
- Handoffs should record both implementation and the artifacts that justified it.

## Verification

- `karakana skill validate-all`
- `karakana skillpack validate-all`
- Focused project tests/evals for the changed scope
