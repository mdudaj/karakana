---
name: interaction-state-design
description: Use this skill when designing, implementing, or auditing UI states for loading, empty, filtered-empty, no-results, error, validation, permission-denied, disabled, readonly, stale-data, async saving, success, conflict, offline, and recovery behavior.
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - interaction states
    - loading state
    - empty state
    - filtered empty
    - no results
    - error state
    - validation state
    - permission denied
    - disabled state
    - stale data
    - async state
    - success state
    - offline state
    - recovery action
  required_files: []
  optional_tools:
    - grep
    - pytest
    - browser-test
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - frontend_design_system_change
  - accessibility_pattern_change
  - workflow_state_contract_change
  - permission_change
---
# Interaction State Design

## Purpose

Guide agents to design, implement, and audit complete UI state behavior so
interfaces remain clear, accessible, recoverable, and task-oriented across
loading, empty, error, permission, async, and workflow-state transitions.

Use this skill to prevent screens that only work in the “happy path.” In
operational systems, users often make decisions under partial data, stale data,
network delay, permission limits, validation failures, or blocked prerequisites.
Those states are part of the product, not edge-case polish.

## When to use this skill

Use for:

- worklists, dashboards, forms, detail pages, tables, filters, search, tabs,
  notifications, dialogs, drawers, and workflow task pages;
- loading, skeleton, progress, empty, filtered-empty, no-results, error,
  validation-error, warning, success, stale-data, offline, blocked, disabled,
  readonly, conflict, permission-denied, and retry/recovery states;
- async interactions such as save, submit, refresh, autocomplete, import,
  background processing, and workflow transition;
- UI state contracts that should become reusable components or design-system
  rules.

## When not to use this skill

Do not use for backend-only changes with no user-visible state. Do not use this
skill to redefine business workflow states; combine with the relevant workflow
or domain skill when changing state machines or process semantics.

For screen hierarchy use `material-hcd-interface`. For reusable component
contracts use `material-component-spec`. For Viewflow form controls use
`viewflow-form-controls`. For accessibility gates use
`accessibility-wcag-audit`. For state copy use `ux-writing`. For browser
evidence of state transitions, filtered states, responsive behavior, or visual
regressions use `design-qa-playwright`. For reusable tokens/components use
`design-system-governance`.

## Quick Reference

- Define states before implementation, not after the happy path renders.
- Separate data state, permission state, workflow state, network state, and UI
  interaction state.
- Empty means no records exist in the current context; filtered-empty means
  records may exist but current filters hide them; no-results means search found
  no match.
- Loading should communicate scope: page, section, row, control, or action.
- Progress indicators must be informative, not decorative.
- Errors should explain what happened, whether work was saved, and the next
  safe action.
- Disabled controls need a reason when the user expects to act.
- Permission-denied states should explain the boundary without exposing
  unauthorized data.
- Stale-data states should show freshness and a refresh/retry path when action
  safety depends on current data.
- Success states should confirm the completed outcome and route to the next
  likely task.
- Status updates and validation messages must be accessible, not only visual.

## Core concepts

- **State inventory**: the explicit set of visible states a screen/component can
  enter.
- **State owner**: which layer decides the state: server/domain, permission,
  workflow engine, network/request, form validation, or client UI.
- **Recovery path**: what the user can safely do next: retry, clear filters,
  request access, refresh, undo, continue, open details, or contact support.
- **Scope of feedback**: feedback should appear where the state occurs: control,
  row, section, page, or shell.
- **State accessibility**: status and errors must be perceivable through text,
  semantics, focus, and assistive technology where relevant.
- **Operational safety**: critical warnings and blocked workflow states should
  not be hidden behind optional panels or decorative-only signals.

## Evidence-backed basis

Read `references/state-patterns.md` before non-trivial state design or audit.

Key source directions:

- Material progress guidance treats progress indicators as communication about
  ongoing processes such as loading, submitting, or saving; they should inform
  users about status and available action.
- Material empty-state guidance distinguishes empty content from failures and
  recommends preventing user confusion with clear, purposeful messaging.
- Material error guidance recommends recovery paths and not offering actions
  that the system already knows cannot work.
- WCAG requires predictable focus/input behavior, text error identification,
  labels/instructions, and programmatically determinable status messages.

## Standard workflow

1. **Classify the surface.** Name the page/component and whether it is a
   dashboard, worklist, form, detail, search/filter surface, or workflow task.
2. **Inventory state sources.** Data, filters/search, permissions, workflow,
   validation, network, background job, integration, and time freshness.
3. **Define the state matrix.** List all states that can appear and who owns
   each one.
4. **Choose Material-compatible patterns.** Skeleton/progress for loading,
   inline messages for local errors, banners for page-level warnings, chips for
   active filters, snackbars/toasts for transient confirmation, dialogs only for
   decisions that require interruption.
5. **Write user-facing state copy.** Use `ux-writing` to state what happened,
   why it matters, and the next safe action. Avoid implementation guidance in
   production UI.
6. **Place feedback by scope.** Control-level state near the control, row state
   in the row, section state in the section, page state below the header, global
   state in the shell.
7. **Define recovery actions.** Retry, refresh, clear filters, start setup,
   request access, open details, undo, continue, or contact support.
8. **Apply accessibility gate.** Status messages, focus movement, keyboard
   recovery, color independence, labels, and error semantics.
9. **Update reusable components.** Use `material-component-spec` to add or
   reuse shared state components instead of page-local markup when the state
   recurs.
10. **Verify.** Add tests or browser checks for happy path and non-happy states.

## Required checks

- Are empty, filtered-empty, no-results, loading, error, validation, permission,
  disabled, stale, success, and conflict states considered?
- Is each state owned by the right layer?
- Does each state explain what happened and the next safe action?
- Are unavailable actions hidden, disabled with reason, or moved deeper based
  on user need and permission?
- Is the feedback placed at the correct scope?
- Does loading/progress indicate the operation scope and avoid blocking more UI
  than necessary?
- Are retry/refresh actions offered only when they can plausibly work?
- Are active filters visible as removable chips when filter state is not
  obvious?
- Does filtered-empty offer clear filters or broaden-search recovery?
- Does permission-denied avoid leaking unauthorized record details?
- Are status and error messages accessible and not color-only?
- Are stale-data indicators present where decisions depend on freshness?
- Are tests/browser checks covering at least one non-happy state?

## Safety rules

- Do not invent business states that are not supported by the domain/workflow
  model.
- Do not hide critical safety, quality, authorization, or workflow-blocking
  states behind optional panels.
- Do not label an unavailable action as “disabled” without confirming whether
  the server also rejects it.
- Do not offer retry when the system can determine retry will fail.
- Do not expose restricted data in empty/error/permission copy.
- Do not use success messages for operations that are only queued unless the
  copy clearly says queued.

## Output format

```markdown
## Interaction State Design

- Surface/job:
- State sources:
- State matrix:
- Material patterns:
- User-facing copy:
- Recovery actions:
- Accessibility checks:
- Reusable components/rules:
- Verification:
- Remaining risk:
```

## Examples

- Worklist with no tasks: distinguish “no tasks exist,” “filters hide tasks,”
  and “search found no matching task.” Show clear-filter recovery for the
  filtered state.
- Viewflow form submit: show submitting state on the submit action, preserve
  entered values on validation failure, announce errors, and confirm the saved
  workflow transition.
- Storage movement blocked: explain the prerequisite or permission boundary,
  link to the actionable setup/review path if permitted, and keep server-side
  enforcement.
- Dashboard refresh: show last-updated metadata, section-level loading if only
  one card reloads, and stale-data warning if action safety depends on freshness.

## Pitfalls

- Designing only the populated happy path.
- Treating empty, filtered-empty, and search no-results as the same state.
- Blocking the whole page for a row/control-level operation.
- Showing walls of disabled actions instead of surfacing ready work.
- Using snackbars for persistent errors that require action.
- Moving implementation rationale into production UI copy.
- Reporting queued/background work as completed.
- Forgetting permission-denied and stale-data states.

## Verification

- `karakana skill validate skills/interaction-state-design`
- `karakana eval run --case skills/interaction-state-design/evals/interaction-state-design.yml`
- `karakana skill validate-all`
- For projects: add render/browser tests for representative non-happy states
  and verify accessibility through `accessibility-wcag-audit`.
