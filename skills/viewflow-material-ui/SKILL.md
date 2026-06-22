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
- Forms must use Viewflow form definitions/rendering inside `vf-form` and `vf-card__form`; do not hand-render Django fields unless extending Viewflow rendering for a missing widget.
- Action cards must be visually consistent across siblings: same icon policy, same content structure, same action region, same button placement level, and same action-button styling.
- Back actions should use a reusable icon+label component that states the destination.

## Purpose

Keep Viewflow/Material applications consistent, accessible, and reusable by turning one-off frontend decisions into shared layout and component rules.

## When to use this skill

Use for any route/page/form/card/tab/navigation implementation or revision in a Viewflow/Material frontend.

## When not to use this skill

Do not use for backend-only tasks with no rendered UI. Do not replace a mature project design system unless the user explicitly requests a redesign.

## Core concepts

- Viewflow already supplies Material Design CSS, templates, and form rendering; project components should extend that foundation.
- Page layout is a grid plus stacked sections, not loose adjacent blocks. Spacing belongs to the page stack or reusable surface abstraction, not incidental margins on one child.
- Page headers own compact navigation/actions such as back icon buttons and secondary links.
- Cards are for grouped actions and summaries; lists/tables are for dense comparison.
- Tabs reduce clutter only when content panels are siblings under the same page concept, and tab markup should follow MDC tab structure.
- Tab panels need structured content such as metric lists, rows, panels, or empty states; avoid punctuation-delimited prose for status data.
- Form pages should have one primary task and one form component.

## Standard workflow

1. Inspect existing project templates and Viewflow templates before adding markup.
2. Identify whether the page is a hub, list, form, detail, or mixed dashboard.
3. Choose reusable abstractions before writing page-specific CSS.
4. Use explicit vertical stack spacing between every major page component; verify sibling sections cannot touch.
5. Put sibling action cards in a consistent action-card grid with equal-height cards and an aligned action region.
6. Put related content panels behind Material/MDC tabs when stacked cards/lists would clutter the page.
7. Style active tab indicators at the bottom unless the project explicitly defines another placement.
8. Style tab panel contents as structured summaries, not loose text separated by punctuation.
9. Put form content in a full-width Viewflow/Material form card and render fields through Viewflow layouts unless a narrow form is explicitly required.
10. Put labeled back actions and secondary action links in the page header action area.
11. Add tests/assertions for durable UX rules that can regress.

## Safety rules

- Do not hide required access control behind navigation only; protect routes too.
- Do not use icon-only back actions when the destination should be clear; use a visible label.
- Do not use placeholders instead of visible labels.
- Do not create page-specific component variants when a reusable abstraction is appropriate.
- Do not mix custom tab markup with Material tabs when MDC tab classes are available.
- Do not hand-render ordinary Django form fields in Viewflow projects; define a Viewflow layout and render it.

## Required checks

- Does the page have visible vertical spacing between every major sibling component?
- Does the page use the right page type: hub, list, form, detail, or tabbed content?
- Are tabs built with `mdc-tab-bar`, `mdc-tab`, `mdc-tab__content`, `mdc-tab-indicator`, and URL/ARIA-backed panels?
- Is the active tab indicator below the tab label by default?
- Is tab panel content structured with reusable styling rather than punctuation-delimited prose?
- Are sibling cards consistent in icon use, content layout, action-region structure, and button placement?
- Are sibling action buttons consistent in Material styling and icon policy?
- Are forms built with Viewflow/Material wrappers, Viewflow layouts, and visible labels?
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

## Pitfalls

- Adjacent sections touching because spacing only lives on one component or an unreliable incidental margin.
- Mixing icon cards and non-icon cards in the same action group.
- Mixing icon action buttons and text-only action buttons in the same sibling card group.
- Letting action-card buttons drift to different vertical positions because cards do not share an action region.
- Leaving tab content as raw semicolon-separated text.
- Putting secondary forms or review lists inside a single-purpose form page.
- Adding raw Django form markup instead of a reusable Material/Viewflow wrapper.
- Creating custom tabs when MDC tabs are the expected Material pattern.

## Verification

- Render tests for key text, routes, and absence of forbidden fields.
- CSS/template search for reusable component classes and MDC tab/form classes.
- Focused Django tests for access and route behavior.
