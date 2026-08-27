---
name: hcd-ui-ux-delivery-loop
description: Use this skill for UI/UX work that must be researched, specified, implemented, critiqued, and refined until it meets a defined human-centered design, Material, accessibility, and design-system quality threshold.
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - HCD UI delivery
    - UX delivery loop
    - UI refinement threshold
    - critique after delivery
    - refine until pass
    - human centered UI
    - Material UX audit
    - screenshot critique loop
    - design quality gate
  required_files: []
  optional_tools:
    - grep
    - pytest
    - browser-test
    - web_search
allowed_tools:
  - read_file
  - grep
  - code_search
  - web_search
  - run_tests
requires_approval_for:
  - design_system_contract_change
  - frontend_design_system_change
  - accessibility_pattern_change
  - navigation_information_architecture_change
  - frontend_test_infrastructure_change
---
# HCD UI/UX Delivery Loop

## Purpose

Make UI/UX delivery repeatable and evidence-grounded. Use this skill when an
agent must move from research and screenshot critique to implementation, then
review the rendered result and refine it until it reaches a stated quality
threshold.

This skill coordinates specialist skills. It does not replace
`material-hcd-interface`, `visual-design-review`, `material-component-spec`,
`viewflow-material-ui`, `viewflow-form-controls`, `ux-writing`,
`accessibility-wcag-audit`, `interaction-state-design`, or
`design-qa-playwright`.

## When to use this skill

Use for:

- broad UI/UX work where the user asks for research, HCD, Material alignment,
  critique, and refinement;
- screenshot-based critique that should result in implementation-ready
  guidelines or a reusable project rule;
- repeated misses in layout, spacing, filter styling, KPI cards, action
  placement, empty states, audit lists, dashboards, worklists, help pages, or
  Viewflow forms;
- work where the user expects the agent to refine the delivered UI until a
  measurable threshold is met;
- creation or revision of project UX standards that should guide future agents.

## When not to use this skill

Do not use for backend-only changes. Do not use it for a tiny copy or CSS fix
unless the defect exposes a reusable design-system rule. Do not load every
specialist UX skill by default; use `ux-skill-router` to choose the smallest
set needed for the slice.

## Quick Reference

- Before implementing UI, produce behavior and look-and-feel requirements.
- Before implementing UI, verify that a project style-organization contract
  exists for page identity, layout stack, action lanes, filters, rows/cards,
  empty states, and responsive behavior. If it does not exist, create or update
  that guidance first.
- If existing project guidance does not cover the feature, gather targeted HCD,
  Material, accessibility, and domain evidence before implementation.
- Use project tokens, components, templates, and Viewflow conventions. Avoid
  page-local styling for repeated problems.
- After implementation, inspect rendered evidence, score the result, and refine
  before delivery if the threshold is not met.
- For screenshot critique, explain the task impact of each issue; do not
  present taste as fact.
- For dense review surfaces such as audit trails, prioritize scanability,
  evidence clarity, consistent event taxonomy, filters as chips, semantic
  status, and secondary export/review actions.

## Core concepts

- **User job**: the user’s operational goal, not the page’s database model.
- **Evidence baseline**: project design-system guidance plus targeted external
  research when local guidance is missing.
- **UX requirements**: behavior requirements and look-and-feel requirements
  written before implementation.
- **Rendered evidence**: browser-visible proof such as screenshots, DOM checks,
  Playwright flows, accessibility checks, or manual screenshot inspection.
- **Quality threshold**: a scorecard and blocker gate that decides whether the
  UI is deliverable or must be refined.
- **Refinement loop**: critique the rendered result, fix P0/P1 issues, rerun
  checks, and only then summarize delivery.

## Research-backed basis

Use current project guidance first. When it is missing or too weak, ground the
decision in authoritative sources:

- Material 3 for component roles, layout, surfaces, state layers, and adaptive
  composition.
- WCAG 2.2 for accessibility requirements such as labels, focus, target size,
  predictable behavior, status messages, and error identification.
- GOV.UK Service Manual and Design System for simple, inclusive services,
  task-oriented content, consistency, and user-tested patterns.
- Nielsen Norman Group heuristics for visibility of system status, real-world
  language, consistency, error prevention, recognition over recall, minimalist
  design, and task-focused help.
- Domain evidence such as SOPs, LIMS workflows, audit expectations, regulated
  review needs, and screenshots from the current system.

For scoring and pass/fail rules, read `references/review-threshold.md`.

For cross-project style organization, page identity, and consistency gates,
read `references/style-organization.md`.

## Standard workflow

1. **Classify the work.** State whether the task is critique-only, plan-only,
   implementation, post-delivery QA, or project design-system governance.
2. **State users and environment.** Name the roles, work pressure, device
   context, domain risk, and the primary question the screen must answer.
3. **Inspect local evidence.** Read existing project UX specs, templates,
   components, tokens, screenshots, tests, and relevant skills.
4. **Check style organization.** Confirm the project has reusable guidance or
   components for page identity, layout spacing, action lanes, filters,
   rows/cards, empty states, and responsive behavior. If missing, create or
   update the style organization rule before editing the page.
5. **Research only the missing guidance.** If local guidance is absent for the
   feature, gather focused HCD, Material, accessibility, and domain references.
6. **Route specialist skills.** Choose one primary skill and only required
   support skills:
   - `material-hcd-interface` for screen hierarchy and Material composition;
   - `visual-design-review` for screenshot critique and visual hierarchy;
   - `material-component-spec` for reusable component anatomy;
   - `design-token-system` for color, type, spacing, density, radius,
     elevation, and focus tokens;
   - `viewflow-material-ui` for Viewflow page templates and Material structure;
   - `viewflow-form-controls` for generated workflow forms and complex fields;
   - `interaction-state-design` for loading, empty, error, disabled,
     permission, stale, and success states;
   - `ux-writing` for labels, actions, empty states, errors, help, and
     notifications;
   - `accessibility-wcag-audit` for keyboard, focus, labels, contrast, ARIA,
     targets, and status messages;
   - `design-qa-playwright` for rendered browser verification.
7. **Write requirements.** Define behavior requirements and visual
   requirements before editing. Include state coverage and acceptance criteria.
8. **Implement through reusable surfaces.** Prefer shared components, tokens,
   templates, and documented patterns over page-local CSS.
9. **Verify mechanically.** Run relevant tests, validators, Playwright/browser
   flows, accessibility checks, and screenshot capture where available.
10. **Critique the rendered result.** Use the scorecard in
   `references/review-threshold.md` and classify findings as P0/P1/P2/P3.
11. **Refine until threshold.** Fix P0/P1 issues and any failed score gates
    before claiming delivery. If blocked, report the exact blocker and the next
    verification step.
12. **Document the rule.** If the issue is reusable, update the relevant skill,
    component spec, design-system doc, or durable memory so it does not recur.

## Audit UI review guidance

Audit screens are evidence-review workspaces. They should quickly answer:

- What happened?
- Who did it?
- When did it happen?
- Was it successful, failed, corrected, exported, or reviewed?
- Which object, route, or workflow did it affect?
- What requires follow-up?

For audit trails:

- make search and filters compact; use filter chips for selected constraints;
- move advanced filters into a clear “More filters” path;
- keep export, retention, and review actions secondary to event review;
- use a dense list or table with clear columns for event, actor, object,
  outcome, time, and action;
- normalize event names into user-readable labels while preserving raw event
  codes in detail views;
- use semantic accents for outcome/category, not the same warning tone for all
  rows;
- keep row actions consistent, such as “View details” or “Open source”;
- avoid nested cards that make empty states and forms heavier than the event
  evidence;
- keep pagination, timestamps, and counts visible and predictable.

## Required checks

- Has the user-facing job been stated before critique or implementation?
- Have behavior requirements and look-and-feel requirements been written before
  editing?
- Has existing project guidance been checked first?
- Does a style-organization contract exist for page identity, layout stack,
  action lanes, filters, rows/cards, empty states, and responsive behavior?
- If guidance was missing, is the HCD/design research source-backed?
- Are Material components used by semantic role, not just visual appearance?
- Are repeated visual issues addressed through reusable tokens/components?
- Are filters, tabs, cards, empty states, actions, and audit rows consistent
  with the project design system?
- Are accessibility risks checked against WCAG, especially labels, focus,
  keyboard access, target size, contrast, and status/error messaging?
- Has rendered evidence been inspected or tested after implementation?
- Does the result meet the pass threshold in
  `references/review-threshold.md`?
- If the threshold is not met, has the agent refined the result or reported a
  concrete blocker?

## Safety rules

- Do not let visual simplification hide required warnings, audit evidence,
  permissions, validation, or workflow state.
- Do not treat interface hiding as authorization.
- Do not make cross-project or global design-system changes without explicit
  scope and verification.
- Do not claim a UI passes from code inspection alone when rendered evidence is
  available and relevant.
- Do not commit generated screenshot, protocol, or runtime artifacts.

## Output format

```markdown
## HCD UI/UX Delivery Loop

- Work type:
- User-facing job:
- Evidence used:
- Specialist skills:
- Requirements:
- Implementation boundary:
- Rendered verification:
- Score:
- Findings/refinements:
- Pass/fail:
- Remaining risk:
- Recommended next task:
```

## Pitfalls

- Starting from component aesthetics instead of the operator’s next decision.
- Overloading a dashboard or audit page with every possible action.
- Treating filters as the main page task.
- Using chips, badges, cards, tables, or tabs for appearance rather than their
  Material role.
- Fixing one page when the issue is a reusable component or token gap.
- Accepting “looks better” without a threshold, screenshot evidence, and
  accessibility checks.
- Starting UI implementation when the project has no reusable rule for page
  identity, action organization, filter styling, and list/card anatomy.

## Examples

- Audit trail critique: route through this skill, inspect screenshots, use
  `visual-design-review` for hierarchy/density findings, use
  `material-hcd-interface` for the evidence-review page structure, require
  filter chips and semantic row states, verify with browser evidence, then
  score against `references/review-threshold.md`.
- Page header inconsistency: before moving icons or changing title spacing,
  check or create the project page identity rule. The page icon, title,
  subtitle, and action lane should come from a shared pattern rather than
  page-local header markup.
- Viewflow workflow form with date/time fields: use this skill only if the work
  includes the full research/specification/refinement loop; otherwise route
  directly to `viewflow-form-controls`, `accessibility-wcag-audit`, and
  `design-qa-playwright`.
- Repeated dashboard card defects: use this skill when the user expects a
  global rule and post-delivery critique; route reusable card anatomy to
  `material-component-spec` and token decisions to `design-token-system`.

## Verification

- `karakana skill validate skills/hcd-ui-ux-delivery-loop`
- `karakana eval run --case skills/hcd-ui-ux-delivery-loop/evals/hcd-ui-ux-delivery-loop.yml`
- `karakana skill validate-all`
- `karakana skillpack validate-all`
