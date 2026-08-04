---
name: system-design-thinking
description: Use this skill before consequential platform, UX, workflow, access-control, reporting, integration, performance, or architecture work where changes affect multiple actors, components, data paths, permissions, feedback loops, or operational incentives. Use when the user asks for system design thinking, systems thinking, robust design, end-to-end platform thinking, unintended consequences, leverage points, or a systematic plan grounded in best practices and research. Skip for small isolated code fixes, one-file cosmetic changes, or already-specified implementation tasks that do not alter system behavior.
version: 0.1.0
risk_level: medium
category: productivity
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
    - system design thinking
    - systems thinking
    - platform design
    - end-to-end design
    - leverage points
    - unintended consequences
    - operating model
    - workflow architecture
    - role-based UX
    - access-control UX
  required_files: []
  optional_tools:
    - grep
    - git
allowed_tools:
  - read_file
  - grep
  - code_search
  - web_search
  - run_tests
requires_approval_for:
  - durable_architecture_decision_change
  - schema_contract_change
  - permission_change
  - production_deployment
  - safety_policy_change
---
# System Design Thinking

## Purpose

Guide consequential product, platform, UX, workflow, and architecture planning
through a whole-system pass before proposing implementation. The skill makes an
agent map actors, data, permissions, feedback loops, delays, failure paths, and
leverage points so changes improve the operating system rather than only a
local screen or component.

## When to use this skill

Use before work that changes or plans:

- platform shell, navigation, dashboard, or role-specific UX;
- user management, authorization, onboarding, audit, or permission flows;
- reporting, exports, analytics, Power BI, or data-quality workflows;
- workflow state machines, review cycles, queues, synchronization, or offline
  behavior;
- integrations, deployment flows, environment transfer, or performance
  architecture;
- cross-project patterns, design-system rules, skills, protocols, or durable
  architecture decisions.

## When not to use this skill

Do not use for:

- tiny, isolated code fixes with no broader behavior change;
- straightforward implementation already covered by accepted artifacts;
- short factual answers;
- code review of an existing diff, unless the diff changes system behavior.

Use `grill-with-docs` to stress-test an existing plan against documents. Use
`brainstorm-verbalized-sampling` when several materially distinct strategies
need option generation and scoring. Use `delivery-artifact-gate` before
implementation to confirm required artifacts.

## Quick Reference

Run these phases in order:

1. Boundary
2. Actors and Jobs
3. Structure
4. Dynamics and Delays
5. Leverage Points
6. Design Rules
7. Delivery Slices
8. Backfire Risks
9. Synthesis

Do not jump to leverage points before structure and dynamics are explicit.

## Core concepts

- Local optimizations can harm the wider operating system when actors,
  incentives, permissions, data freshness, or feedback loops are ignored.
- A system has structure before it has leverage points: map actors, flows,
  states, and trust boundaries before proposing interventions.
- Delays change behavior. Slow feedback, stale projections, pending approvals,
  and cache lag can make technically correct features feel broken.
- Design rules are the bridge from thinking to delivery; they must be checkable
  in code, artifacts, tests, evals, or operational runbooks.
- Slices should improve the system in reversible steps, not depend on a large
  future redesign.

## Standard workflow

### 1. Boundary

State:

- system in focus;
- purpose from the primary stakeholder view;
- in scope;
- out of scope;
- assumptions that require evidence.

If the boundary is unclear, ask at most three scoping questions. If progress is
still possible, proceed with labeled working assumptions.

### 2. Actors and Jobs

Identify each relevant actor and their job-to-be-done:

- primary users;
- administrators;
- reviewers/approvers;
- support or operations staff;
- external systems;
- regulators, auditors, or governance owners where relevant.

For each actor, record goal, pain/risk, permissions, and success signal.

### 3. Structure

Map the system pieces:

- key entities and data flows;
- permissions and trust boundaries;
- workflow states and transitions;
- UI surfaces and route ownership;
- integration points;
- queues, caches, projections, or background processors;
- source-of-truth records versus derived views.

Use short `From -> To: what moves` lines for important flows.

### 4. Dynamics and Delays

Identify:

- reinforcing loops;
- balancing loops;
- bottlenecks;
- hidden dependencies;
- time lags between action and effect;
- places where users may receive stale, missing, or misleading feedback.

If a loop does not apply, say so and explain why.

### 5. Leverage Points

For each candidate lever, state:

- leverage point;
- why it matters;
- expected effect;
- risk of backfire;
- evidence needed;
- reversibility.

Prefer levers that improve information flow, rules, feedback, permissions,
state clarity, and incentives before adding more UI or automation.

### 6. Design Rules

Turn the system analysis into durable rules:

- UX organization rules;
- data visibility rules;
- state and feedback rules;
- permission and audit rules;
- performance and loading rules;
- failure and recovery rules;
- documentation or artifact rules.

Each rule should be specific enough that a later implementation can be checked.

### 7. Delivery Slices

Sequence implementation into reversible slices:

- slice goal;
- prerequisites;
- implementation boundary;
- non-goals;
- verification;
- rollback or fallback.

Deliver the smallest slice that improves the system without depending on
unproven future work.

### 8. Backfire Risks

Name unintended consequences:

- role confusion;
- hidden permission leaks;
- misleading metrics;
- slow startup;
- fragile manual processes;
- audit gaps;
- operational workarounds;
- support burden.

For each material risk, include a mitigation or decision gate.

### 9. Synthesis

End with:

- concise system story;
- recommended direction;
- rejected tempting local optimizations;
- exact next action;
- artifacts that must be created or updated before implementation.

## Pitfalls

- Jumping from a visible symptom to a page-local fix.
- Treating hidden navigation as permission enforcement.
- Adding metrics without source-of-truth and freshness rules.
- Optimizing startup by hiding necessary feedback or loading stale data.
- Creating broad platform visions without a small next slice.
- Writing an ADR for every minor detail while missing the actual system
  decision.
- Treating this skill as a substitute for requirements, ADRs, tests, or
  approval gates.

## Safety rules

- Do not use this skill to bypass approval gates for permissions, production,
  schema, safety, authentication, or deployment.
- Do not treat UI hiding as authorization.
- Do not invent research findings; cite project evidence or official/current
  references when claims are unstable.
- Do not propose unsupported metrics, unsupported progress denominators, or
  unapproved automation.
- Do not create architecture decisions silently; route durable decisions through
  the project's ADR or artifact process.
- Preserve project-specific safety rules and explicit user decisions.

## Required checks

- Boundary is explicit.
- Actors and jobs are named.
- Data, permission, workflow, and UI structures are mapped.
- Dynamics, delays, and feedback loops were considered.
- Leverage points include backfire risk and reversibility.
- Design rules are checkable.
- Delivery slices include non-goals and verification.
- Authorization, data visibility, audit, and performance risks were checked.
- Required follow-up artifacts are named.

## Verification

- Confirm the response includes every phase from Boundary through Synthesis.
- Confirm approval-sensitive changes are still gated.
- Confirm role, permission, data visibility, audit, and performance risks were
  explicitly considered where relevant.
- Confirm the next slice has non-goals and verification.
- Confirm any durable rules are routed to project artifacts, ADRs, skills, or
  validators instead of remaining only in chat.

## Output format

```markdown
# System Design Thinking

## Boundary

## Actors and Jobs

## Structure

## Dynamics and Delays

## Leverage Points

## Design Rules

## Delivery Slices

## Backfire Risks

## Synthesis
```

## Examples

- Before redesigning a dashboard, map user roles, work queues, data freshness,
  visibility, startup cost, exception flow, and reporting dependencies.
- Before adding self-service user onboarding, map identity provider, contact,
  invitation, mailbox, audit, assignment, permissions, and fallback flows.
- Before optimizing performance, map critical startup path, lazy-loaded
  surfaces, data volume, cache behavior, user-perceived feedback, and risk of
  stale metrics.
