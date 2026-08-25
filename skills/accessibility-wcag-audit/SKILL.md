---
name: accessibility-wcag-audit
description: Use this skill when reviewing, planning, implementing, or verifying web UI accessibility against WCAG, WAI-ARIA, keyboard, focus, contrast, labels, forms, status messages, target size, and automated/manual audit expectations.
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - accessibility
    - WCAG
    - a11y
    - axe
    - keyboard navigation
    - screen reader
    - focus state
    - contrast
    - labels
    - ARIA
    - target size
    - accessible forms
    - Playwright accessibility
  required_files: []
  optional_tools:
    - grep
    - pytest
    - browser-test
    - playwright
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - accessibility_pattern_change
  - frontend_design_system_change
  - permission_change
---
# Accessibility WCAG Audit

## Purpose

Guide agents to plan, implement, and audit accessible web interfaces using WCAG,
WAI guidance, Material-compatible interaction states, and project verification
gates. The default target is WCAG 2.2 AA unless a project, law, contract, or
client requirement sets a stricter profile.

Use this skill as the accessibility gate for `material-hcd-interface`,
`design-system-governance`, `viewflow-material-ui`,
`viewflow-form-controls`, `material-component-spec`, `design-token-system`,
`visual-design-review`, `interaction-state-design`, and `ux-writing`.

## When to use this skill

Use for any user-facing UI work involving:

- forms, custom controls, autocomplete, dialogs, drawers, date pickers, tabs,
  tables, menus, notifications, dashboards, or worklists;
- accessibility review, WCAG conformance planning, or regression prevention;
- keyboard navigation, focus order, focus visibility, color contrast, labels,
  ARIA roles/states/properties, status messages, target size, and error
  handling;
- browser tests using axe, Playwright, or project-specific render checks.
- stateful UI behavior planned through `interaction-state-design`, especially
  status messages, validation, loading, error, stale, permission, and success
  states.
- reusable component contracts planned through `material-component-spec`.
- token changes planned through `design-token-system`, especially contrast,
  focus, disabled, warning, error, and status token pairs.
- visual critique from `visual-design-review` that may mask accessibility risk.
- labels, instructions, error text, status messages, and confirmation copy from
  `ux-writing`.
- browser execution and evidence plans from `design-qa-playwright` when
  accessibility checks should run through Playwright/axe or keyboard flows.

## When not to use this skill

Do not use for backend-only changes with no rendered interface. Do not treat an
automated scan as complete conformance evidence; automated checks catch common
issues but manual keyboard, semantics, copy, and user-flow review remain needed.

## Quick Reference

- Target WCAG 2.2 AA by default; document any lower or stricter target.
- Prefer semantic HTML and framework-native accessible components before custom
  ARIA. Bad ARIA is worse than no ARIA.
- Every control needs a programmatic name, visible label where practical, role,
  value/state, focus path, and error/help association.
- Keyboard-only users must be able to reach, operate, escape, and recover from
  every interactive control.
- Focus must be visible, not obscured, and must move predictably.
- Text and meaningful UI states must not rely only on color.
- Status messages, async results, validation errors, and successful actions
  should be perceivable without stealing focus unnecessarily.
- Target sizes and spacing must support pointer use in real work environments.
- For forms, ask only what is required, group related fields, provide
  instructions, validate input, and show recovery paths.
- Use automated checks as a gate, then perform manual checks for flows and
  custom controls.

## Core concepts

- **Conformance target**: the project’s declared WCAG version and level.
  Default to WCAG 2.2 AA for new work.
- **Accessible name/role/value**: assistive technologies need each control’s
  identity, purpose, state, and value.
- **Keyboard operability**: every interaction must work without a mouse,
  including opening/closing popups, selecting options, submitting, cancelling,
  and recovering from errors.
- **Focus management**: focus order follows task order; focus is visible;
  dialogs/sheets trap and restore focus; route changes place focus usefully.
- **Perceivable feedback**: loading, success, error, warning, filtered-empty,
  selected, disabled, and readonly states must be visible and programmatically
  available when relevant.
- **Manual-plus-automated audit**: axe/Playwright findings are useful gates but
  do not replace manual review or inclusive usability testing.

## Research-backed basis

Read `references/wcag-ui-audit.md` for the checklist and source mapping before
non-trivial UI accessibility work.

Key source directions:

- W3C WCAG 2.2 adds criteria including focus not obscured, dragging
  alternatives, target size minimum, consistent help, redundant entry, and
  accessible authentication.
- W3C WAI forms guidance emphasizes labels, grouping, instructions, validation,
  notifications, and shorter forms.
- WAI-ARIA APG combobox guidance defines popup behavior, keyboard interaction,
  and ARIA expectations for autocomplete-like controls.
- Playwright recommends axe scans as useful automated checks while explicitly
  noting that many accessibility issues require manual assessment.

## Standard workflow

1. **Declare scope and target.** Name page/control/flow, user roles, device
   context, and WCAG target.
2. **Inventory interactive elements.** List links, buttons, fields, tabs,
   chips, menus, tables, dialogs, popups, notifications, and custom controls.
3. **Check semantic foundation.** Prefer native elements; verify name, role,
   value, headings, landmarks, labels, groups, and relationships.
4. **Check keyboard path.** Tab order, arrow-key behavior, Enter/Space,
   Escape, popup/dialog behavior, focus restoration, and no keyboard trap.
5. **Check visual accessibility.** Contrast, focus visibility, target size,
   text scaling, responsive clipping, color independence, reduced motion, and
   density.
6. **Check forms and validation.** Labels, help, required meaning, errors,
   summaries, recovery, redundant entry, and preserved values.
7. **Check dynamic state.** Loading, async completion, errors, status messages,
   no-results, filtered-empty, stale data, disabled/readonly, and permission
   states.
8. **Check custom controls.** Confirm ARIA pattern, keyboard support, popup
   ownership, active descendant/selection state, and screen-reader labels.
9. **Verify with tools.** Run focused automated scans where available and add
   manual/browser assertions for issues automation cannot prove.
10. **Record findings by severity.** Use P0 for blocking/no access, P1 for
    serious task failure, P2 for degraded access, P3 for polish or future
    improvement.

## Required checks

- Is the WCAG target declared?
- Are headings and landmarks meaningful?
- Does each control have accessible name, role, value, and visible purpose?
- Can the task be completed with keyboard only?
- Is focus visible, ordered by task flow, and restored after dialogs/popups?
- Are overlays, drawers, dialogs, menus, and date pickers dismissible with
  keyboard?
- Are labels, fieldsets/groups, help text, and errors associated with fields?
- Are status messages announced or programmatically determinable where needed?
- Does the UI avoid color-only communication?
- Do contrast and disabled/readonly states remain legible?
- Are pointer targets and spacing safe for the work environment?
- Are animations/motion safe and reducible?
- Are autocomplete/combobox controls tested against WAI-ARIA expectations?
- Are automated scan results paired with manual keyboard/flow review?

## Safety rules

- Do not claim WCAG conformance from an automated scan alone.
- Do not add ARIA roles that contradict native element semantics.
- Do not remove visible labels to make a screen look cleaner.
- Do not hide focus outlines without replacing them with an equally visible
  project focus style.
- Do not expose unauthorized records through accessibility labels, hidden text,
  autocomplete suggestions, or DOM-only content.
- Do not weaken security/authentication to satisfy accessibility; design an
  accessible secure path instead.

## Output format

```markdown
## Accessibility WCAG Audit

- Scope:
- WCAG target:
- High-risk controls/flows:
- Automated checks:
- Manual keyboard checks:
- Semantics/ARIA:
- Forms/validation:
- Visual accessibility:
- Findings by severity:
- Required fixes:
- Verification:
- Remaining risk:
```

## Examples

- A Viewflow autocomplete field must expose a label, editable combobox behavior,
  suggestion list semantics, keyboard selection, clear state, no-results state,
  scoped server suggestions, and submit-time validation.
- A task form date picker must allow keyboard entry, picker selection, visible
  format help, focus restoration, and field-level error recovery.
- A dashboard alert strip must not rely only on color; its status should be
  clear by text, icon semantics where useful, and readable contrast.
- A modal approval flow must trap focus while open, close on Escape when safe,
  restore focus to the invoking control, and announce validation/status changes.

## Pitfalls

- Equating Material styling with accessibility.
- Treating axe as complete proof.
- Creating custom controls before trying native controls.
- Using placeholder-only labels.
- Making focus invisible for visual polish.
- Showing errors only as color changes.
- Adding keyboard shortcuts without discoverability or collision checks.
- Forgetting filtered-empty, no-results, network-error, and permission-denied
  states.

## Verification

- `karakana skill validate skills/accessibility-wcag-audit`
- `karakana eval run --case skills/accessibility-wcag-audit/evals/accessibility-wcag-audit.yml`
- `karakana skill validate-all`
- For projects: run focused render/browser tests and automated accessibility
  scans where available; manually verify keyboard flow for custom controls.
