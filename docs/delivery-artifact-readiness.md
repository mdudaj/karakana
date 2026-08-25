# Delivery Artifact Readiness

## Purpose

Prevent repeated work by making durable delivery artifacts part of the definition of ready and definition of done for Karakana-managed projects.

## Rule

Before implementation starts, the agent must identify the required artifact set for the work type. Before delivery is marked complete, the agent must verify that every required artifact exists or record a narrow not-applicable rationale in the PR, handoff, or delivery note.

Chat instructions can authorize a task, but they do not replace durable project artifacts when the work needs requirements, ADRs, milestone instructions, delivery instructions, UX requirements, schemas, examples, tests, evals, or handoffs.

## Artifact Convention

Use evidence-backed artifacts, not freeform intent. A non-trivial task should have enough structure for a different agent to execute it without rereading the whole conversation.

| Artifact | Purpose | Required when |
| --- | --- | --- |
| Product requirements document (PRD) | Problem, users, outcomes, scope, non-goals, UX, architecture, data, safety, acceptance criteria, and verification context. | A slice has user-visible behavior, multiple implementation surfaces, cross-cutting impact, or multi-agent handoff risk. |
| Requirements note | Narrow behavior, look-and-feel, constraints, evidence, and acceptance requirements. | A full PRD is too heavy but behavior or UX still needs durable scope. |
| User stories | Actor, goal, outcome, INVEST check, dependencies, and acceptance criteria. | Work delivers user-visible or operator-visible capability. |
| Acceptance criteria / Definition of Done | Testable pass/fail conditions and completion evidence. | Any behavior-changing task. |
| Requirements traceability | Requirement-to-story-to-design-to-code-to-test links. | Work spans UX, architecture, data/schema, safety, or multiple files/agents. |
| UX description | Before/after workflow, states, look and feel, accessibility, responsive behavior, and design-system fit. | Visible workflow, form, screen, dashboard, navigation, copy, or layout changes. |
| ADR / decision record | Context, decision, alternatives, consequences, rollback, and verification. | Durable or hard-to-reverse architecture, workflow, schema, provider, identity, or safety decision. |
| Schema/example contract | Data shape, API, generated artifact, import/export, fixture, or eval evidence. | Data, schema, API, package, or generated artifact changes. |
| Artifact readiness | Definition-of-ready and definition-of-done checklist with paths and not-applicable rationale. | Before non-trivial implementation and before declaring delivery complete. |

## Evidence Standard

Every material requirement should cite one of:

- direct user input;
- project contract, durable memory, OKF concept, ADR, existing docs, or issue;
- code, schema, fixture, trace, eval, or runtime artifact;
- task-specific research or best-practice source;
- explicit assumption labeled as an assumption with validation path.

PRDs and requirements notes should avoid unsupported claims. If evidence is missing, record an open question or assumption rather than inventing a requirement.

## Minimum Check

For every non-trivial slice, answer these questions before editing and again before final delivery:

- What artifact states the user-facing or system behavior requirement?
- What artifact states the acceptance criteria and definition of done?
- What PRD or requirements note records users, goals, non-goals, constraints, and evidence?
- What traceability artifact links requirements to stories, UX/ADR/schema decisions, implementation surfaces, and tests/evals?
- What milestone, roadmap, or delivery instruction bounds this slice?
- What ADR or decision record justifies durable architecture, workflow, schema, data, identity, safety, or provider choices?
- What schemas, examples, fixtures, or manifests define produced data artifacts?
- What tests or evals prove the required behavior and prevent regression?
- What handoff records the changed artifacts, verification, residual risks,
  remaining tasks or known follow-ups, the recommended next task, and exact
  next action?

## UX Check

If the work changes a visible workflow, page, form, dashboard, interaction, copy, navigation, or layout, the required artifact set also includes:

- behavior requirements;
- look-and-feel requirements;
- current best-practice research for the delivered task;
- alignment notes for the existing design system;
- render or screenshot evidence when feasible.

If the work starts a new product, portal, major UX refresh, or first implementation slice, the UX artifact set must also establish or reference:

- app shell layout and route ownership;
- navigation groups and page/action placement rules;
- design tokens for color, type, spacing, radius, elevation, focus, and density;
- reusable component inventory and component anatomy;
- responsive behavior for desktop, tablet, and mobile;
- accessibility rules and interaction states;
- visual evidence such as mockups, screenshots, or comparable product references.

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
