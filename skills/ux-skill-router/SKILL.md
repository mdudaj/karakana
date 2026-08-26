---
name: ux-skill-router
description: Route UX/UI tasks to the right Karakana design-system skills and sequence them for Material, human-centered design, Viewflow frontend, accessibility, UX writing, and Playwright verification work.
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - UX skill
    - UI skill
    - design system skill
    - route UX work
    - which design skill
    - interface skill catalogue
    - frontend skill sequence
    - Material HCD
    - Viewflow frontend UX
    - design-system workflow
  required_files: []
  optional_tools:
    - grep
    - pytest
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - design_system_policy_change
  - cross_project_skill_change
  - frontend_test_infrastructure_change
---
# UX Skill Router

## Purpose

Route interface work to the smallest useful set of Karakana UX/UI skills and
put them in the right order. Use this skill when a task is broad, ambiguous, or
could touch more than one UX discipline: human-centered design, Material
components, design tokens, Viewflow frontend forms, accessibility, writing,
state behavior, or browser QA.

This is an index and sequencing skill. It does not replace the specialist
skills; it decides which ones to load and why.

## When to use this skill

Use for:

- deciding which UX/UI skill applies to a request;
- planning a frontend slice that may involve more than one design discipline;
- turning screenshot critique into implementation-ready skill routing;
- reviewing whether a proposed UI change needs component, token, accessibility,
  writing, Viewflow, state, or browser-test coverage;
- constructing a reusable delivery protocol for UX work across projects.

## When not to use this skill

Do not use for backend-only work with no user-facing interface. Do not load
every design skill by default. Route to the minimal specialist set needed for
the task.

## Quick Reference

Read `references/router-matrix.md` when the task is non-trivial or when more
than one route may apply.

- Screenshot critique, visual hierarchy, density, grouping, polish:
  `visual-design-review`.
- Whole screen structure, task hierarchy, HCD, Material page composition:
  `material-hcd-interface`.
- Repeated UI pattern, reusable component anatomy, variants, states:
  `material-component-spec`.
- Color, typography, spacing, radius, elevation, density, theme, focus tokens:
  `design-token-system`.
- Shared design-system policy or cross-page consistency:
  `design-system-governance`.
- Viewflow templates, page layout, cards, tabs, shell, route chrome:
  `viewflow-material-ui`.
- Viewflow/Django form controls, AJAX selects, date/time pickers, formsets,
  dynamic workflow fields: `viewflow-form-controls`.
- Loading, empty, filtered-empty, error, permission, stale, disabled, success,
  async states: `interaction-state-design`.
- Labels, actions, helper text, validation, empty states, notifications, help
  text, navigation names: `ux-writing`.
- WCAG, keyboard, focus, contrast, labels, status messages, ARIA semantics:
  `accessibility-wcag-audit`.
- Playwright browser evidence, DOM assertions, screenshots, responsive checks,
  visual regression, axe execution: `design-qa-playwright`.
- Missing project/skill guidance for a UI pattern, work environment, or feature:
  perform research-backed HCD first, then route the finding to the relevant
  specialist skill.
- Broad UI/UX delivery where the user expects research, specification,
  implementation, critique, and refinement until a quality gate passes:
  `hcd-ui-ux-delivery-loop`.

## Core concepts

- **Primary skill**: the specialist skill that owns the main user-facing risk.
- **Supporting skill**: a secondary skill needed because the task affects
  another concern, such as accessibility, writing, tokens, state, or browser QA.
- **Skill sequence**: the order in which skills should be applied so critique,
  specification, implementation, and verification happen coherently.
- **Minimal routing**: loading only the skills needed for the current slice.
- **Rendered evidence**: browser-visible proof that the implemented interface
  behaves and appears as specified.
- **Design-system boundary**: the line between a page-local change and a
  reusable component, token, or governance rule.

## Standard workflow

1. **State the user-facing job.** Identify what the operator, reviewer, manager,
   or administrator is trying to accomplish.
2. **Classify the concern.** Decide whether the main issue is hierarchy,
   visual critique, component anatomy, token mapping, Viewflow implementation,
   form controls, interaction state, writing, accessibility, browser QA, or
   governance.
3. **Check available guidance.** Use existing project UX specs, design-system
   contracts, component rules, and loaded skills first. If the feature or
   interaction pattern is not covered, perform research-backed HCD before
   planning implementation.
4. **Choose one primary skill.** Pick the skill that owns the highest-risk or
   most central concern.
5. **Add only necessary support skills.** Add supporting skills for concrete
   secondary risks, not because they are available.
6. **Define the implementation boundary.** State what is in scope, what remains
   unchanged, and whether the fix should be page-local or reusable.
7. **Define evidence before delivery.** Name required tests, screenshots,
   accessibility checks, or review artifacts.
8. **Report unused skills.** For broad requests, explicitly list tempting skills
   that were intentionally not used and why.

## Default sequences

Use the shortest sequence that covers the risk.

### Screenshot critique to implementation

1. `hcd-ui-ux-delivery-loop` when the user expects critique plus delivery and
   a pass/fail threshold; otherwise start with `visual-design-review`
2. `material-hcd-interface` if page hierarchy changes
3. `material-component-spec` or `design-token-system` if the fix is reusable
4. `accessibility-wcag-audit` if labels, focus, contrast, forms, or custom
   controls are affected
5. `design-qa-playwright` for rendered evidence before delivery

### Viewflow form/control work

1. `viewflow-form-controls`
2. `ux-writing` for labels, help, validation, and action text
3. `interaction-state-design` for async, validation, permission, or success
   states
4. `accessibility-wcag-audit` for keyboard/focus/label checks
5. `design-qa-playwright` for browser interaction verification

### New reusable component

1. `material-component-spec`
2. `design-token-system` if visual values or token mappings change
3. `interaction-state-design` for non-happy states
4. `accessibility-wcag-audit`
5. `design-qa-playwright`

### Cross-page/global styling issue

1. `hcd-ui-ux-delivery-loop` when the issue includes delivery/refinement gates
2. `design-system-governance`
3. `visual-design-review` to classify impact
4. `material-component-spec` or `design-token-system` depending on cause
5. `design-qa-playwright` for affected-page evidence

### UX copy/content issue

1. `ux-writing`
2. `material-hcd-interface` if copy affects page hierarchy or task flow
3. `accessibility-wcag-audit` if labels, errors, instructions, or status
   messages are affected
4. `design-qa-playwright` when critical copy should be asserted in browser
   tests

## Required checks

- What is the user-facing job or risk?
- Is the request visual critique, screen structure, reusable component, token,
  form/control, state, accessibility, writing, browser QA, or governance?
- Which specialist skill is primary?
- Does this task require a post-delivery critique threshold through
  `hcd-ui-ux-delivery-loop`?
- Which secondary skills are necessary, and why?
- Which tempting skills are not needed for this slice?
- Does the task need requirements/look-and-feel notes before implementation?
- If existing project/skill guidance does not cover the feature, has
  research-backed HCD evidence been gathered and recorded before delivery?
- Does the task affect a shared pattern that should be documented rather than
  patched page-locally?
- What verification evidence is required before delivery?

## Safety rules

- Do not use routing as permission to broaden the user's requested change.
- Do not route every UI task to every UX skill.
- Do not let visual polish override authorization, workflow safety, audit
  requirements, data integrity, or server-side validation.
- Do not approve screenshot baseline updates, CI changes, or cross-project
  design-system changes without explicit approval.
- Do not commit generated runtime protocol/eval artifacts.

## Pitfalls

- Loading every UX skill for routine work.
- Starting with implementation before identifying the primary user-facing job.
- Delivering UI/UX from taste or habit when no project guidance exists instead
  of doing targeted HCD/design research first.
- Treating screenshot critique as only CSS polish when it exposes component,
  token, state, or writing gaps.
- Hiding unavailable actions without checking route/service permissions.
- Writing page-local CSS for a repeated design-system problem.
- Skipping browser evidence for changes that users will judge visually or
  interactively.

## Output format

```markdown
## UX Skill Routing

- User-facing job:
- Primary skill:
- Supporting skills:
- Skills intentionally not used:
- Required requirements/spec notes:
- Research/HCD evidence:
- Implementation boundary:
- Verification evidence:
- Remaining risk:
```

## Examples

- “The task filter UI is ugly”: start with `visual-design-review`, then route
  to `material-component-spec` for chips/toolbar if reusable, and
  `design-qa-playwright` for rendered evidence.
- “Research HCD, implement the UI revision, critique the delivered result, and
  refine until it passes”: start with `hcd-ui-ux-delivery-loop`, then load only
  the specialist skills it routes to.
- “Add a calendar control to workflow forms”: start with
  `viewflow-form-controls`, add `accessibility-wcag-audit`, `ux-writing`, and
  `design-qa-playwright`.
- “KPI cards have inconsistent icon sizing”: start with
  `material-component-spec`, use `design-token-system` for sizing tokens, then
  browser-check with `design-qa-playwright`.
- “Navigation names confuse lab users”: start with `ux-writing`, then
  `material-hcd-interface` if route hierarchy changes.

## Verification

- `karakana skill validate skills/ux-skill-router`
- `karakana eval run --case skills/ux-skill-router/evals/ux-skill-router.yml`
- `karakana skill validate-all`
- `karakana skillpack validate-all`
