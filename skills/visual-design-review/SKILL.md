---
name: visual-design-review
description: Use this skill when critiquing or auditing a user interface for visual hierarchy, layout, spacing, density, typography, component consistency, Material alignment, design-system adherence, accessibility risk, and implementation-ready findings.
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - visual design review
    - UI critique
    - UX critique
    - visual hierarchy
    - layout critique
    - spacing critique
    - density
    - typography hierarchy
    - visual polish
    - design review
    - screenshot review
    - Material review
    - HCD review
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
  - visual_identity_change
---
# Visual Design Review

## Purpose

Guide agents to critique and audit user interfaces with professional visual
design judgment while staying implementation-ready: hierarchy, grouping,
spacing, density, typography, Material component semantics, state clarity,
accessibility risk, and reusable design-system fixes.

Use this skill when a user shares a screenshot, asks whether a screen “looks
right,” or reports repeated visual issues such as cramped KPI cards, touching
sections, unclear tabs, weak icons, poor filter styling, over-nested surfaces,
or inconsistent actions.

## When to use this skill

Use for:

- screenshot or browser review of dashboards, worklists, forms, detail pages,
  landing pages, help pages, setup pages, and operational screens;
- critique of visual hierarchy, spacing, grouping, density, typography, color,
  icons, cards, surfaces, tabs, filters, empty states, tables, and action
  placement;
- turning subjective visual feedback into concrete component/token/state
  changes;
- deciding whether a UI issue belongs in screen hierarchy, component spec,
  tokens, accessibility, interaction state, or framework implementation.

## When not to use this skill

Do not use for backend-only work. Do not use it to invent a new brand identity;
use `design-token-system` and project brand guidance for that. Do not implement
visual fixes directly from opinion; route repeated or systemic issues to the
right reusable skill.

Combine with:

- `material-hcd-interface` for screen/task hierarchy;
- `material-component-spec` for reusable component contracts;
- `design-token-system` for color/type/spacing/density tokens;
- `interaction-state-design` for non-happy states;
- `accessibility-wcag-audit` for WCAG/accessibility gates;
- `design-qa-playwright` for rendered browser evidence, screenshots,
  responsive checks, and visual regression QA;
- `ux-writing` for labels, buttons, errors, empty states, confirmations, and
  help text;
- `viewflow-material-ui` for Viewflow/Material implementation.

## Quick Reference

- Start with the user’s job and screen type, then critique visual execution.
- Review from top priority to lowest priority: attention, ready action, primary
  content, supporting controls, metadata, secondary details.
- Separate issues into hierarchy, grouping, spacing, density, typography, color,
  component anatomy, states, accessibility, and implementation contract.
- Use proximity and common-region principles before adding more borders.
- Use Material surface hierarchy: not every section needs a heavy outline.
- Keep primary actions visually stronger than filters and secondary controls.
- Visual critique must produce implementation-ready changes, not vague taste
  comments.
- Route systemic fixes to tokens/components/partials, not page-local CSS.
- Route unclear labels, errors, empty states, and action text through
  `ux-writing`.
- Identify what to keep, what to change, and what to remove.

## Core concepts

- **Visual hierarchy**: the order in which the eye discovers content and
  actions.
- **Grouping**: whether related elements appear related through proximity,
  similarity, common region, or alignment.
- **Density**: how much information appears per area without harming scanning,
  touch/click safety, or comprehension.
- **Surface hierarchy**: how backgrounds, cards, elevation, borders, and
  whitespace communicate containment and priority.
- **Component anatomy**: whether repeated UI pieces have consistent internal
  regions such as icon, title/value, supporting text, status, and action.
- **Review severity**: the practical impact of a visual issue on task success,
  error risk, speed, confidence, or maintainability.

## Evidence-backed basis

Read `references/review-heuristics.md` before non-trivial critique.

Key source directions:

- Material accessibility guidance emphasizes placing items according to
  importance and keeping related items of similar hierarchy near each other.
- Material theming guidance treats color and type as hierarchy tools; primary
  roles should be reserved for important actions and type roles should match
  purpose.
- WCAG requires predictable focus/order, error identification, labels, status
  messages, and consistent identification. Visual hierarchy must not conflict
  with accessible order.
- Baymard’s UX methodology weights findings by observed severity and frequency;
  Karakana reviews should similarly prioritize high-impact blockers before
  polish.
- Public UI-agent skills separate critique/design review from tokens,
  component specs, accessibility, and implementation adapters.

## Standard workflow

1. **Identify evidence.** Use screenshot/browser view, route, viewport, role,
   design-system docs, and comparable screens.
2. **Classify screen/job.** Dashboard, worklist, form, detail, setup, help,
   review, or mixed screen.
3. **State the intended hierarchy.** What should the user notice first, second,
   and third?
4. **Audit visual hierarchy.** Check title, primary work area, actions, metrics,
   filters, alerts, metadata, and secondary content.
5. **Audit grouping and spacing.** Check proximity, alignment, common regions,
   page stack gaps, nested surfaces, and touching controls.
6. **Audit component anatomy.** Check repeated cards/rows/filters/tabs/buttons
   for consistent slots, icon size, value/text hierarchy, and action placement.
7. **Audit typography and color.** Check type scale, weight, line height,
   contrast, semantic color restraint, and whether color reflects meaning.
8. **Audit states and accessibility risk.** Check focus order, labels, target
   size, non-color cues, empty/loading/error states, disabled reasons, and
   status messages.
9. **Prioritize findings.** P0/P1/P2/P3 by task impact, error risk, frequency,
   and implementation scope.
10. **Route fixes.** Screen hierarchy, component spec, tokens, state design,
    accessibility, Viewflow implementation, or copy.
11. **Define reviewable slices.** Prefer one coherent slice with acceptance
    criteria and verification over scattered visual patches.

## Required checks

- Does the screen answer the user’s next-decision question quickly?
- Is the primary content/action visually dominant?
- Do filters, metadata, and secondary actions avoid competing with the main
  work?
- Are related elements grouped by proximity/alignment/common region?
- Are page sections separated by reusable stack spacing?
- Are there too many nested borders/cards/surfaces?
- Are repeated components anatomically consistent?
- Are icons intentional in size, alignment, and semantic role?
- Are typography roles clear and not cramped?
- Are semantic colors meaningful and restrained?
- Does visual order match keyboard/focus/task order?
- Are non-happy states represented or explicitly planned?
- Is unclear or implementation-centric UI copy routed through `ux-writing`?
- Are findings routed to reusable tokens/components/states instead of
  page-local CSS?
- Does the review identify which findings require browser evidence through
  `design-qa-playwright` before delivery?

## Safety rules

- Do not present personal taste as objective fact; tie critique to task impact,
  design-system rules, accessibility, or maintainability.
- Do not copy another product’s proprietary visual identity.
- Do not remove important warnings, labels, focus indicators, or permission
  cues for visual minimalism.
- Do not suggest global CSS/token changes without checking likely affected
  components.
- Do not let screenshot polish override server-side permissions, workflow
  safety, or audit requirements.

## Output format

```markdown
## Visual Design Review

- Screen/job:
- Evidence reviewed:
- What works:
- Main issue:
- Findings by severity:
- Recommended changes:
- Skill routing:
- Acceptance criteria:
- Verification:
- Remaining risk:
```

## Examples

- KPI cards: keep the metric structure, but fix cramped type hierarchy, weak
  icon sizing, inconsistent semantic accents, and tokenize card anatomy.
- Task page filters: move secondary filters behind `More filters`, show active
  chips, separate tabs from the toolbar, and verify filtered-empty state.
- Landing page: remove catalogues of unavailable actions, promote ready work,
  keep attention states conditional, and summarize storage/quality modules.
- Help page: make search primary, common tasks actionable, reference content
  progressively disclosed, and troubleshooting intent-based.

## Pitfalls

- Saying “looks bad” without naming task impact.
- Fixing every screenshot with isolated CSS.
- Adding borders to solve grouping when spacing would work.
- Making all cards equally prominent.
- Treating filters as primary actions.
- Ignoring focus/accessibility while reviewing visual order.
- Failing to identify what should remain unchanged.

## Verification

- `karakana skill validate skills/visual-design-review`
- `karakana eval run --case skills/visual-design-review/evals/visual-design-review.yml`
- `karakana skill validate-all`
- For projects: browser/screenshot review at representative viewports, focused
  DOM/component assertions, and accessibility checks where relevant.
