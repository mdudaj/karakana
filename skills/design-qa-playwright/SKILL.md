---
name: design-qa-playwright
description: "Use this skill when planning, writing, or auditing browser-based UI verification with Playwright: rendered evidence, screenshots, visual comparisons, DOM assertions, accessibility scans, responsive checks, state coverage, and regression protocols."
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - Playwright
    - browser test
    - visual regression
    - screenshot test
    - UI QA
    - design QA
    - DOM assertion
    - accessibility scan
    - axe
    - responsive test
    - end to end UI
    - rendered evidence
  required_files: []
  optional_tools:
    - grep
    - pytest
    - playwright
    - browser-test
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - frontend_test_infrastructure_change
  - screenshot_baseline_update
  - accessibility_gate_change
  - ci_workflow_change
---
# Design QA Playwright

## Purpose

Guide agents to verify user-facing interface work with browser evidence:
Playwright interactions, user-facing locators, DOM assertions, screenshots,
visual comparisons, accessibility scans, responsive checks, and state coverage.

Use this skill when UI work needs proof beyond unit tests or template tests. It
turns “looks good locally” into repeatable review evidence while avoiding
flaky, overbroad, or screenshot-only tests.

## When to use this skill

Use for:

- visual/design-system changes that need rendered evidence;
- browser tests for forms, worklists, dashboards, navigation, filters, tabs,
  dialogs, drawers, autocomplete, date pickers, notifications, and stateful UI;
- screenshot baselines or visual comparisons;
- DOM/component assertions for reusable UI contracts;
- accessibility scans with axe/Playwright;
- responsive checks across compact, medium, and expanded viewports;
- end-to-end UI reviews before delivery.

## When not to use this skill

Do not use for backend-only behavior that can be verified with faster unit or
integration tests. Do not rely only on screenshots when a semantic DOM/assertion
would be more stable. Do not update screenshot baselines without explicit
review/approval when the baseline is committed.

Combine with:

- `visual-design-review` for critique findings;
- `material-hcd-interface` for screen hierarchy;
- `material-component-spec` for component acceptance criteria;
- `interaction-state-design` for non-happy state coverage;
- `accessibility-wcag-audit` for accessibility scope;
- `ux-writing` for labels/messages asserted in tests;
- `viewflow-material-ui` and `viewflow-form-controls` for Viewflow screens and
  widgets.

## Quick Reference

- Prefer user-facing locators: role, label, text, alt text, title, then test ID
  only for stable non-user-visible contracts.
- Use auto-retrying Playwright assertions for async UI.
- Test behavior and semantics before screenshot pixels.
- Use screenshots for layout/regression evidence, not as the only correctness
  gate.
- Keep screenshot baselines deterministic: same browser/project, viewport,
  fonts/environment, seeded data, and masked/hidden volatile regions.
- Cover representative states: populated, empty, filtered-empty, loading,
  error, permission-denied, disabled, stale, success, and responsive layout.
- Run axe scans where available, but pair them with manual keyboard/focus checks.
- Store or report artifacts so reviewers know where to inspect.

## Core concepts

- **Rendered evidence**: browser-visible proof such as screenshots, traces,
  DOM assertions, or accessibility reports.
- **Semantic locator**: locator based on accessible role, name, label, or text.
- **DOM contract**: stable assertion that a reusable component exposes expected
  structure/classes/roles/states.
- **Visual baseline**: approved screenshot used for future visual comparison.
- **Volatile region**: timestamp, animation, random data, cursor, notification,
  or external widget that should be stabilized or masked.
- **State coverage**: intentional testing of happy and non-happy UI states.

## Evidence-backed basis

Read `references/playwright-ui-qa.md` before non-trivial browser UI QA.

Key source directions:

- Playwright recommends role, text, label, alt text, title, and test-id
  locators, with role locators closest to how users and assistive technology
  perceive the page.
- Playwright assertions auto-retry until the expected condition is met, which
  reduces flakiness for async UI.
- Playwright supports screenshot visual comparisons through
  `expect(page).toHaveScreenshot()`, but rendering can vary by OS, browser,
  settings, hardware, and headless mode.
- Playwright accessibility testing with axe catches common issues such as
  contrast, missing labels, invalid properties, and duplicate IDs, but automated
  tests do not detect all accessibility problems.

## Standard workflow

1. **Classify verification.** Render smoke, interaction flow, component
   contract, visual regression, accessibility scan, responsive check, or full
   end-to-end review.
2. **Inspect current test harness.** Use project scripts/config first. Do not
   invent a parallel browser test stack if one exists.
3. **Define evidence target.** Name route, role/context, data fixture, viewport,
   state, and artifact expected.
4. **Choose stable assertions.** Prefer role/label/text assertions and DOM
   contracts before screenshot comparison.
5. **Cover states.** Include at least one meaningful non-happy state when the
   UI change affects states.
6. **Check interactions.** Click/type/select/keyboard through the actual user
   path, including back/cancel/retry/clear actions when relevant.
7. **Check accessibility.** Run axe if available and manually verify keyboard
   and focus behavior for custom controls.
8. **Use screenshots carefully.** Stabilize viewport/data/fonts, hide volatile
   regions, name baselines clearly, and require review before updating committed
   baselines.
9. **Record evidence.** Report command, route, viewport, role/context, result,
   artifact path, and unresolved risks.
10. **Keep tests maintainable.** Avoid brittle selectors, sleeps, broad pixel
    snapshots, and assertions that duplicate implementation details without
    user or component value.

## Required checks

- Is there an existing project browser-test command to use?
- Are locators based on role/label/text before test IDs?
- Do assertions auto-wait instead of relying on fixed sleeps?
- Are screenshots limited to visual/layout evidence that DOM assertions cannot
  cover well?
- Are volatile regions stabilized, masked, or excluded?
- Are compact/medium/expanded viewports checked when layout changes?
- Are non-happy states checked when state behavior changes?
- Are form/control interactions checked with keyboard where relevant?
- Are axe/accessibility scans paired with manual keyboard/focus review?
- Is screenshot baseline update explicit and reviewable?
- Are artifacts named and reported for reviewers?

## Safety rules

- Do not update committed screenshot baselines without explicit approval or a
  clearly accepted UI change.
- Do not add sleeps as the primary synchronization mechanism.
- Do not use brittle CSS/XPath selectors when user-facing locators are possible.
- Do not claim accessibility conformance from axe alone.
- Do not put secrets, private data, or production records into screenshots,
  traces, snapshots, or test fixtures.
- Do not make CI/deployment workflow changes without explicit approval.

## Output format

```markdown
## Design QA Playwright Plan

- UI change under test:
- Routes/states/viewports:
- Data/role context:
- Assertions:
- Screenshots:
- Artifacts:
- Accessibility:
- Commands:
- Baseline policy:
- Verification:
- Remaining risk:
```

## Examples

- Task filter QA: assert search field by label, more-filters button by role,
  active filter chips by text, clear action behavior, filtered-empty copy, and
  screenshots at desktop/compact widths.
- KPI card QA: assert card count, semantic labels, icon containers, tokenized
  classes, loading/error states, and one stable screenshot.
- Viewflow form QA: fill fields by label, exercise AJAX select, pick/enter date,
  submit, verify validation and success/queued state, run axe, and check focus.
- Help page QA: assert search-first entry, common task links, glossary route,
  support route, and responsive layout.

## Pitfalls

- Screenshot-only tests for semantic behavior.
- Pixel baselines over large dynamic pages.
- Fixed sleeps after clicks.
- CSS selectors coupled to incidental DOM.
- Ignoring failed keyboard paths because mouse tests pass.
- Updating baselines to hide regressions.
- Capturing production/private data in artifacts.

## Verification

- `karakana skill validate skills/design-qa-playwright`
- `karakana eval run --case skills/design-qa-playwright/evals/design-qa-playwright.yml`
- `karakana skill validate-all`
- For projects: run the project’s browser-test command, inspect generated
  screenshots/traces, and record artifact paths in the delivery summary.
