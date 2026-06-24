# Delivery Artifact Readiness

## Purpose

Prevent repeated work by making durable delivery artifacts part of the definition of ready and definition of done for Karakana-managed projects.

## Rule

Before implementation starts, the agent must identify the required artifact set for the work type. Before delivery is marked complete, the agent must verify that every required artifact exists or record a narrow not-applicable rationale in the PR, handoff, or delivery note.

Chat instructions can authorize a task, but they do not replace durable project artifacts when the work needs requirements, ADRs, milestone instructions, delivery instructions, UX requirements, schemas, examples, tests, evals, or handoffs.

## Minimum Check

For every non-trivial slice, answer these questions before editing and again before final delivery:

- What artifact states the user-facing or system behavior requirement?
- What artifact states the acceptance criteria and definition of done?
- What milestone, roadmap, or delivery instruction bounds this slice?
- What ADR or decision record justifies durable architecture, workflow, schema, data, identity, safety, or provider choices?
- What schemas, examples, fixtures, or manifests define produced data artifacts?
- What tests or evals prove the required behavior and prevent regression?
- What handoff records the changed artifacts, verification, residual risks, and exact next action?

## UX Check

If the work changes a visible workflow, page, form, dashboard, interaction, copy, navigation, or layout, the required artifact set also includes:

- behavior requirements;
- look-and-feel requirements;
- current best-practice research for the delivered task;
- alignment notes for the existing design system;
- render or screenshot evidence when feasible.

If none of those UX surfaces change, record that UX is not involved.

## Delivery Blockers

Do not mark the work complete when:

- required artifacts are missing and no not-applicable rationale is recorded;
- implementation names or output artifacts diverge from requirement or schema docs without updating those docs;
- tests pass but acceptance criteria are missing;
- a PR summary omits changed artifacts, verification, risks, or remaining gaps;
- the handoff does not identify exact next action and residual artifact gaps.

## PR Summary Requirement

For non-trivial work, PR bodies and final delivery notes should include:

- reused artifacts;
- new or updated artifacts;
- not-applicable artifacts with rationale;
- verification commands and results;
- unresolved risks or follow-up gaps.

## Verification

Use the relevant protocol check when a trace is active, then run project-specific validation such as:

```bash
karakana skill validate-all
karakana skillpack validate-all
python -m pytest
```
