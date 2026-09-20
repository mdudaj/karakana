---
name: viewflow-material-ui
description: Use this skill when designing or implementing frontend pages, forms, action cards, tabs, spacing, or navigation in a Viewflow/Material-based application, including reusable UI abstractions that should generalize across projects.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - pytest
requires_approval_for:
  - frontend_design_system_change
  - accessibility_pattern_change
  - workflow_navigation_change
activation:
  keywords:
    - frontend
    - UI
    - UX
    - Viewflow
    - Material
    - form
    - card
    - tab
    - spacing
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
---
# Viewflow Material UI

## Quick Reference

- Use Viewflow/Material vocabulary first: `mdc-layout-grid`, `mdc-card`, `vf-card`, `vf-form`, `vf-card__form`, `mdc-button`, `mdc-icon-button`, `mdc-tab-bar`, `mdc-tab`, and `mdc-tab-indicator`.
- Project wrappers may extend these classes, but must remain reusable across pages and projects.
- Every page stacks major components with explicit vertical spacing between sibling components.
- Use Material tabs to switch between related content panels when stacked summary/list components would clutter the page; if Viewflow does not provide a ready tab component, create a reusable MDC tab abstraction.
- Active tab styling belongs below the tab label by default; only move it elsewhere when a project rule explicitly says so.
- Forms must use Viewflow form definitions/rendering inside `vf-form` and `vf-card__form`; use `viewflow-form-controls` for normal widgets, AJAX selects, date/time pickers, dynamic workflow forms, and complex validation behavior.
- Login, invitation, and activation pages must still follow Viewflow/Material product UX. Use `viewflow/base.html` or `viewflow/base_page.html`, MDC buttons/cards/tabs where applicable, icon field wrappers where the project has established them, and role/organization-scope copy when access is invite-first.
- Action cards must be visually consistent across siblings: same icon policy, same content structure, same action region, same button placement level, and same action-button styling.
- Back actions should use a reusable icon+label component that states the destination.
- Child/detail/form routes should expose the parent return action near the page
  identity. Bottom Cancel actions are not enough on their own because users
  need the hierarchy cue before interacting with the form or evidence page.
- Keep parent-return navigation structurally separate from page action
  toolbars. In Viewflow/MDC headers, use a dedicated leading/header slot for
  Back/Up and reserve the trailing action group for operations.
- Route-level pages should use a shared page identity/header pattern for icon,
  title, subtitle, optional metadata, and page actions. Do not implement
  page-local icon/title/subtitle styling when a reusable header class or
  component exists.

## Purpose

Keep Viewflow/Material applications consistent, accessible, and reusable by turning one-off frontend decisions into shared layout and component rules.

## When to use this skill

Use for any route/page/form/card/tab/navigation implementation or revision in a Viewflow/Material frontend.

## When not to use this skill

Do not use for backend-only tasks with no rendered UI. Do not replace a mature project design system unless the user explicitly requests a redesign. For screenshot/visual critique, combine with `visual-design-review`; for reusable component contracts, combine with `material-component-spec`; for token work, combine with `design-token-system`; for detailed form-control decisions, combine with `viewflow-form-controls`; for UI state behavior, combine with `interaction-state-design`; for accessibility review, combine with `accessibility-wcag-audit`; for rendered browser evidence, screenshot checks, responsive checks, and end-to-end UI verification, combine with `design-qa-playwright`.

## Core concepts

- Viewflow already supplies Material Design CSS, templates, and form rendering; project components should extend that foundation.
- Use `ux-skill-router` before broad Viewflow UI work when the change may also
  require visual critique, component contracts, tokens, accessibility,
  interaction states, writing, or Playwright evidence.
- Page layout is a grid plus stacked sections, not loose adjacent blocks. Spacing belongs to the page stack or reusable surface abstraction, not incidental margins on one child.
- Page headers own compact navigation/actions such as back icon buttons and secondary links.
- Cards are for grouped actions and summaries; lists/tables are for dense comparison.
- Tabs reduce clutter only when content panels are siblings under the same page concept, and tab markup should follow MDC tab structure.
- Tab panels need structured content such as metric lists, rows, panels, or empty states; avoid punctuation-delimited prose for status data.
- Form pages should have one primary task and one form component. Complex controls such as autocomplete selects, date/time pickers, dependent fields, formsets, and generated workflow fields should be planned with `viewflow-form-controls`.
- Access pages are part of the workflow surface. In enterprise SSO systems, preserve the visible flow: invite → activation → SSO login → application role and organization scope. Bootstrap/local login should be visually secondary when enterprise SSO is the intended path.

## Standard workflow

1. Inspect existing project templates and Viewflow templates before adding markup.
2. Identify whether the page is a hub, list, form, detail, or mixed dashboard.
3. Choose reusable abstractions before writing page-specific CSS.
4. Use the shared page identity/header pattern for route-level icon, title,
   subtitle, and action lane before styling page content.
5. Use explicit vertical stack spacing between every major page component; verify sibling sections cannot touch.
6. Put sibling action cards in a consistent action-card grid with equal-height cards and an aligned action region.
7. Put related content panels behind Material/MDC tabs when stacked cards/lists would clutter the page.
8. Style active tab indicators at the bottom unless the project explicitly defines another placement.
9. Style tab panel contents as structured summaries, not loose text separated by punctuation.
10. Put form content in a full-width Viewflow/Material form card and render fields through Viewflow layouts unless a narrow form is explicitly required; apply `viewflow-form-controls` for widget/control selection.
11. For login/invite/activation pages, compare against the closest mature Viewflow project before editing and enforce the access model in route behavior, not only in navigation.
12. Put labeled back actions and secondary action links in the page header action area.
13. Use shared search-control partials for list/worklist filtering. Do not copy
    MDC text-field search markup route by route; the component should own the
    leading icon, label, value binding, density, and focus treatment.
14. Add tests/assertions for durable UX rules that can regress.

## Safety rules

- Do not hide required access control behind navigation only; protect routes too.
- Do not use icon-only back actions when the destination should be clear; use a visible label.
- Do not use placeholders instead of visible labels.
- Do not create page-specific component variants when a reusable abstraction is appropriate.
- Do not mix custom tab markup with Material tabs when MDC tab classes are available.
- Do not hand-render ordinary Django form fields in Viewflow projects; define a Viewflow layout and render it. For missing widget behavior, create a reusable Viewflow form-control adapter rather than page-local markup.
- Do not let SSO auto-signup bypass invite activation, role assignment, or organization/branch scoping when those are required by the product.

## Required checks

- Does the page have visible vertical spacing between every major sibling component?
- Does the page use the right page type: hub, list, form, detail, or tabbed content?
- Does the route-level page identity use the shared icon/title/subtitle/action
  lane pattern?
- Has visual critique been translated through `visual-design-review` before making broad Viewflow template/CSS changes?
- Are tabs built with `mdc-tab-bar`, `mdc-tab`, `mdc-tab__content`, `mdc-tab-indicator`, and URL/ARIA-backed panels?
- Is the active tab indicator below the tab label by default?
- Is tab panel content structured with reusable styling rather than punctuation-delimited prose?
- Are sibling cards consistent in icon use, content layout, action-region structure, and button placement?
- Do repeated Viewflow/MDC patterns have a `material-component-spec` contract instead of page-local markup?
- Are shared visual values routed through `design-token-system` instead of Viewflow page-local CSS literals?
- Are sibling action buttons consistent in Material styling and icon policy?
- Are forms built with Viewflow/Material wrappers, Viewflow layouts, and visible labels?
- Are complex form controls planned with `viewflow-form-controls` and verified for widget state, accessibility, permissions, and server validation?
- Are loading, empty, error, stale-data, permission, disabled, and success states routed through `interaction-state-design`?
- Are accessibility risks routed through `accessibility-wcag-audit` instead of being treated as visual polish?
- Do login/invite/activation pages use Viewflow base templates, MDC controls, reusable field wrappers, and tested invite-first access copy?
- Are child routes equipped with labeled header back actions?
- Are tabs keyboard/link accessible and backed by URLs or anchors?

## Output format

```markdown
## Viewflow Material UI Check

- Page type:
- Reusable abstractions used:
- Header actions:
- Spacing/layout:
- Cards/tabs/forms:
- Accessibility checks:
- Tests:
```

## Examples

- Curriculum hub: top action-card grid, then a separate Material tab surface for source/snapshot status panels.
- Add source route: header back action plus one full-width Viewflow/Material form card rendered through a Viewflow layout.
- Snapshot capture route: header back action and optional review link, then one full-width form component.
- Enterprise SSO login: primary Microsoft/Entra CTA, secondary bootstrap disclosure, invite activation view, and user-management tabs built with MDC/Viewflow structure.

## Pitfalls

- Adjacent sections touching because spacing only lives on one component or an unreliable incidental margin.
- Mixing icon cards and non-icon cards in the same action group.
- Mixing icon action buttons and text-only action buttons in the same sibling card group.
- Letting action-card buttons drift to different vertical positions because cards do not share an action region.
- Leaving tab content as raw semicolon-separated text.
- Putting secondary forms or review lists inside a single-purpose form page.
- Adding raw Django form markup instead of a reusable Material/Viewflow wrapper.
- Creating custom tabs when MDC tabs are the expected Material pattern.
- Treating authentication/invitation pages as throwaway templates outside the design system.

## Verification

- Render tests for key text, routes, and absence of forbidden fields.
- CSS/template search for reusable component classes and MDC tab/form classes.
- Focused Django tests for access and route behavior.
