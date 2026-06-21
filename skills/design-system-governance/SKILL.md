---
name: design-system-governance
description: Use this skill before frontend work that affects visual consistency, spacing, colors, layout, reusable components, page surfaces, forms, tabs, cards, or cross-project UI rules, especially when repeated UI corrections indicate the project lacks a single design-system source of truth.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - pytest
requires_approval_for:
  - design_system_contract_change
  - frontend_design_system_change
  - accessibility_pattern_change
  - cross_project_rule_change
activation:
  keywords:
    - design system
    - style consistency
    - spacing
    - tokens
    - reusable components
    - frontend governance
    - cards
    - tabs
    - forms
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
---
# Design System Governance

## Quick Reference

- One project, one design-system profile: tokens, surfaces, page stack, tabs, forms, cards, buttons, tables, navigation, and cache/version rules.
- Build UI from reusable components or partials first; page templates compose them.
- Preserve project-specific visual identity through tokens, not one-off page colors.
- Every major page component must be separated by reusable spacing.
- Sibling cards must share anatomy: icon region, content region, action region, and aligned actions.
- Sibling action buttons must share styling and icon policy; if one action button in the sibling group has an icon, all should.
- Forms must use the project framework's canonical renderer; in Viewflow projects, use Viewflow layouts/rendering.
- Tabs must use the project framework's Material component structure; active indicators belong below the tab label by default unless a project explicitly defines otherwise.
- Back actions must use a reusable labeled component that communicates the destination, not only an icon.
- UI work is not done until visual/design-system checks pass on affected pages.

## Purpose

Prevent repeated frontend corrections by making each project declare and enforce a durable UI contract. This skill governs the system around components: where rules live, how components are reused, how project identity stays consistent, and how regressions are caught.

## When to use this skill

Use before implementing or revising frontend pages, especially when the user reports inconsistent spacing, buttons, colors, tabs, forms, cards, or visual style across pages or projects.

## When not to use this skill

Do not use for backend-only changes, text-only copy edits, or tiny visual fixes already covered by an existing component contract. If the change reveals a repeated rule gap, use this skill.

## Core concepts

- Design systems are a contract, not just CSS.
- Tokens carry project identity; components carry reusable behavior and anatomy.
- Page templates should compose components instead of restyling them.
- Cross-project rules define structure and verification; project tokens define the local look.

## Core Rule

Do not fix repeated UI problems with page-local CSS. First identify or create the reusable design-system rule, then patch the shared component/token/partial and add assertions or visual checks that prove the rule.

## Design-System Contract

Each UI project should have a durable contract covering:

- **Tokens**: color, typography, spacing, radius, elevation, focus rings, component heights.
- **Page layout**: content grid, page stack spacing, full-width surfaces, responsive breakpoints.
- **Surfaces**: cards, form surfaces, tab surfaces, table/list surfaces, panels.
- **Components**: buttons, icon buttons, tabs, action cards, form cards, status chips, tables.
- **Anatomy**: required slots/regions for each component, such as action-card icon/body/action.
- **Navigation actions**: reusable back action with icon, label, destination, and accessible text.
- **Framework mapping**: canonical framework classes and renderers, such as Viewflow/MDC classes.
- **Project identity**: which tokens carry the project's palette/style and which component rules are shared.
- **Verification**: render tests, DOM/class assertions, browser screenshots, and CSS cache/version checks.

## Standard workflow

1. Inspect the existing project UI system: tokens, base templates, shared CSS, component partials, and one mature comparable project when available.
2. Classify the request as token, layout, surface, component, framework-rendering, visual-regression, or governance.
3. Update the durable artifact or skill before page edits when a new general rule is being introduced.
4. Patch shared tokens/components/partials first; update page templates only to compose those components.
5. Add or update tests for DOM contracts that can be asserted cheaply.
6. When the issue is visual spacing/alignment/color, run a browser visual check or screenshot comparison when tooling is available.
7. Version static assets or otherwise invalidate caches when CSS changes must be visible in a running app.
8. Refresh the handoff with changed rules, affected pages, verification, and remaining visual risks.

## Safety rules

- Do not replace a project's established visual identity unless explicitly requested.
- Do not weaken accessibility semantics while abstracting components.
- Do not hide route authorization behind navigation or component state.
- Do not introduce broad CSS resets that can affect unrelated pages without review.
- Do not copy project-specific colors or brand styling across projects as a global rule.

## Required checks

- Is the rule project-specific styling or cross-project component behavior?
- Does the project already have a token/component that should be reused?
- Are affected pages composing the same component anatomy?
- Do style changes use tokens instead of page-local colors?
- Do forms/tabs use the canonical framework renderer/markup?
- Is active tab styling positioned according to the project default, usually the bottom indicator?
- Is there visible spacing between major sibling components?
- Are actions aligned by component anatomy, not by accidental content length?
- Do sibling action buttons use the same styling and icon policy?
- Do back actions include a visible destination label?
- Has the browser/static cache been invalidated for changed CSS?
- Is there a test or visual check that would fail if the regression returns?

## Cross-Project Rule

Cross-project rules should define behavior and anatomy, not force a single palette. For example:

- Shared: page stack spacing exists; action cards have icon/body/action regions; action buttons follow icon parity; forms use framework renderers; tabs use Material/MDC anatomy with bottom active indicators; back actions are labeled.
- Project-specific: colors, typography scale, density, radius, elevation, brand imagery, and route-specific copy.

## Pitfalls

- Repeating the same instruction in chat instead of adding a durable rule.
- Adding a page-specific margin when the project needs a page stack abstraction.
- Styling one tab group while another page still uses custom tab markup.
- Letting tab content become unstyled prose separated by punctuation instead of structured rows, metrics, or panels.
- Fixing action-card button alignment without defining the card anatomy.
- Using icon-only back buttons where a user needs to know the destination.
- Changing colors directly in page CSS instead of tokens.
- Forgetting CSS cache-busting, so the running app still shows stale styles.

## Verification

- Design-system skill/artifact updated for new general rules.
- Focused tests assert reusable DOM/component contracts.
- Browser visual check for spacing, alignment, and color consistency when a page is available.
- Static CSS cache/version behavior verified when the app is already running.

## Output format

```markdown
## Design System Gate

- Project design profile:
- Shared rule affected:
- Project-specific styling affected:
- Reusable components/tokens changed:
- Pages checked:
- Verification:
- Remaining visual risk:
```

## Examples

- Repeated spacing issue: patch page-stack abstraction and test for the page-stack class, then visually inspect affected pages.
- Button alignment issue: define action-card anatomy with an action slot; update all sibling cards to use it.
- Tab status content issue: replace punctuation-delimited prose with a reusable metric/list/panel component.
- Form inconsistency: add a Viewflow layout and render through `{% render form form.layout %}` rather than hand-rendering fields.
- Color drift: move values into project tokens and replace page-local colors.
