---
name: m3-application-shell
description: "Use this skill when designing, implementing, or auditing a Material Design 3 application shell: navigation drawer or rail, top app bar, page/content workspace, action lanes, footer/status areas, responsive adaptation, and Viewflow Material frontend mapping."
version: 0.1.0
risk_level: medium
category: development
scope: bundled
status: experimental
visibility: public
bucket: development
activation:
  keywords:
    - Material 3 app shell
    - M3 application shell
    - app shell
    - navigation drawer
    - navigation rail
    - top app bar
    - side nav
    - application layout
    - Viewflow shell
    - Viewflow Material frontend
    - standard application shell
  required_files: []
  optional_tools:
    - grep
    - pytest
    - web_search
allowed_tools:
  - read_file
  - grep
  - code_search
  - web_search
  - run_tests
requires_approval_for:
  - navigation_information_architecture_change
  - frontend_design_system_change
  - accessibility_pattern_change
  - frontend_test_infrastructure_change
---
# Material 3 Application Shell

## Purpose

Guide agents to design and implement consistent Material Design 3 application
shells for enterprise web systems. Use this skill when the work concerns the
outer product frame: navigation, app bar, route identity, content workspace,
global actions, footer/status, responsive adaptation, and Viewflow Material
frontend mapping.

This skill closes the gap between generic Material component guidance and the
repeatable shell structure needed by systems such as Enterprise MEAL.

## When to use this skill

Use for:

- new application shell design or shell refactoring;
- side navigation, navigation rail, top app bar, page title/action lane, footer,
  and workspace layout;
- route hierarchy and information architecture that affects navigation;
- Viewflow shell/template work where pages must share the same Material frame;
- responsive shell behavior across compact, medium, and expanded layouts;
- repeated feedback that pages look inconsistent because headers, content
  widths, actions, cards, or nav states are implemented page-locally.

## When not to use this skill

Do not use for backend-only work or isolated component fixes inside an already
stable shell. For page hierarchy inside the workspace, combine with
`material-hcd-interface`. For reusable internal components, combine with
`material-component-spec`. For Viewflow forms and widgets, combine with
`viewflow-form-controls`. For final rendered proof, combine with
`design-qa-playwright` where available.

## Quick Reference

- Treat the shell as the stable product frame. Individual pages change inside
  the workspace; the navigation, top bar, action lane, and footer remain
  predictable.
- Define shell regions explicitly: navigation, top app bar, route identity,
  global actions, content workspace, contextual action lane, status/footer, and
  skip/focus landmarks.
- Use Material adaptive layout behavior:
  - compact: modal navigation drawer or bottom navigation when appropriate;
  - medium: navigation rail or compact drawer;
  - expanded: standard drawer or permanent drawer plus full workspace.
- Use a 4 px spacing baseline and 8 px rhythm. Shell gutters and section gaps
  should come from tokens, not page-local nudges.
- Page titles and global actions belong in the shell/header pattern, not inside
  each page’s first content card.
- Use navigation for destinations, not actions. Put actions in app/page/section
  action lanes according to scope.
- Do not turn Administration into a dumping ground for configurable objects.
  If a setup operation belongs to a domain area, expose it as a role-controlled
  page action inside that domain route instead of adding another global
  Administration destination.
- When adapting Viewflow `base_page.html`, explicitly decide which default
  drawer/header controls remain visible. If the product has one topbar
  hamburger for drawer width, hide or override drawer-internal Viewflow toggle
  affordances so the brand area does not appear to enforce another behavior.
- Do not place an organization-context eyebrow immediately after a hamburger.
  The hamburger controls navigation, so the text next to it should be route
  identity or an explicit context control. Organization context belongs in the
  brand area or clearly separated context chips.
- For visible shell CSS/JS changes, use the project's cache-busting convention
  so browser cache does not preserve stale navigation appearance or behavior.
- The selected navigation item must be visible, text-labelled, and accessible;
  do not rely on color alone.
- Preserve content width intentionally. Do not let wide desktop pages become
  unbounded lines of text; use max-widths for reading pages and full-width
  grids for dashboards/tables.
- Distinguish lateral destinations from child routes. Top-level drawer
  destinations should not carry arbitrary page back buttons; child/detail/form
  routes should expose a labeled Up action to their parent route through the
  project’s shared header/back component.
- Choose content surfaces by task. Use navigational lists for homogeneous setup
  destinations, not action-card grids that create unbalanced whitespace when
  the items are not dashboard summaries.
- Use Viewflow/Material primitives where the project uses Viewflow:
  `viewflow/base.html`, `viewflow/base_page.html`, `vf-*`, `mdc-*`, and
  reusable project shell blocks/classes before creating page-local markup.
- Shell copy must use user-facing product language. Avoid implementation
  vocabulary such as harness, protocol, fixture, migration, seed, projection,
  or artifact gate in normal navigation and route headers.

## Core shell model

Use this mental model:

```text
Application
├── Brand / product identity
├── Navigation destinations
├── Top app bar
│   ├── route title
│   ├── route subtitle or status
│   └── global actions
├── Page/content workspace
│   ├── page action lane
│   ├── primary work surface
│   ├── secondary/advanced surfaces
│   └── contextual detail or side sheet
└── Footer/status
    ├── environment/status only when user-relevant
    └── copyright/build/support only when appropriate
```

## Core concepts

- **Application shell**: the persistent product frame around route content.
- **Navigation destination**: a place the user can go, not an operation the
  system performs.
- **Route identity**: title, subtitle/status, icon, breadcrumb/back action, and
  scoped actions for the current route.
- **Action lane**: a predictable region for actions whose scope is page-level
  or route-level.
- **Workspace**: the page-owned content area inside the shell.
- **Adaptive shell**: navigation and workspace behavior that changes
  deliberately across compact, medium, and expanded layouts.

## Research-backed basis

Read `references/material-viewflow-shell-synthesis.md` before non-trivial shell
work. It summarizes the Material 3, Material Web, Android adaptive layout,
Viewflow frontend, accessibility, and HCD evidence that governs this skill.

Use current project guidance first. If it conflicts with Material guidance,
record the product-specific reason and keep the deviation explicit.

## Standard workflow

1. **State users and work context.** Identify the primary roles, device class,
   work pressure, and what the shell must help them find or do.
2. **Inventory destinations.** Separate destinations, grouped destinations,
   frequent actions, admin/setup surfaces, and diagnostics.
3. **Choose adaptive navigation.** Define compact, medium, and expanded
   behavior before implementing desktop styling.
4. **Define shell regions.** Navigation, top app bar, route identity, global
   actions, page action lane, workspace, footer/status, skip link, and focus
   targets.
5. **Map to Viewflow/frontend primitives.** Reuse existing Viewflow templates,
   Material classes, blocks, and project components. Add abstractions only when
   a repeated shell pattern is missing.
6. **Define page contracts.** Pages supply route title, subtitle/status,
   actions, breadcrumbs/back action when needed, and content. Pages do not
   rebuild shell chrome.
7. **Apply tokens.** Shell width, gutters, spacing, typography, surfaces,
   navigation state, elevation, radius, focus, and density use design tokens or
   documented project variables.
8. **Cover states.** Loading, permission-denied, no access, stale data, offline,
   sync/error, collapsed navigation, active route, and responsive state.
9. **Check accessibility.** Landmarks, skip link, visible labels, keyboard
   navigation, focus order, target size, status text, and contrast.
10. **Verify.** Run tests/validators and inspect rendered evidence for at least
    one hub page, one list page, one form page, and one detail page when those
    exist.

## Viewflow Material frontend mapping

- Base shell: prefer `viewflow/base.html` or `viewflow/base_page.html` as the
  root frame when using Viewflow.
- Navigation: use shared navigation data or template blocks; do not duplicate
  side-nav markup across pages.
- Page identity: expose template blocks or context values for icon, title,
  subtitle, breadcrumbs/back action, and actions.
- Forms: render via Viewflow form/layout constructs inside the shared page
  workspace. Do not hand-render ordinary form fields unless creating a reusable
  adapter.
- Workflows: task lists, approval screens, and transition forms must use the
  shell action/identity model so workflow state is visible without custom page
  chrome.
- Tests: assert that pages extend the shared shell and do not define duplicate
  route headers, nav containers, or ad hoc action bars.

## Required checks

- Are navigation items destinations rather than actions?
- Are domain-specific operations exposed as page actions instead of global
  Administration destinations?
- Is route identity owned by the shell/header, not duplicated in page content?
- Are global, page, section, and row actions visually scoped to the objects they
  affect?
- Does the shell define compact, medium, and expanded behavior?
- Are shell dimensions, spacing, typography, state layers, and focus styles
  token-based?
- Does the active destination have text plus visual state?
- Are landmarks, skip links, focus order, and keyboard navigation covered?
- Does the page content use the shell workspace rather than rebuilding the
  frame locally?
- Does Viewflow work use Viewflow/Material templates and wrappers before
  project-specific markup?
- Have unwanted Viewflow default shell affordances been hidden or mapped to the
  agreed product behavior?
- Does the hamburger have adequate contrast, hit area, hover/focus state, and
  spacing from the route title?
- Were shell CSS/JS asset versions updated when visible shell behavior changed?
- Are loading, no-access, permission, stale-data, and sync states visible and
  user-facing?
- Is implementation/backend vocabulary kept out of normal navigation and route
  headers?
- Is there a test, validator, or rendered check that prevents shell regressions?

## Safety rules

- Do not use navigation visibility as authorization.
- Do not hide no-access, permission, sync, or stale-data states for visual
  polish.
- Do not introduce global shell changes without checking representative pages.
- Do not put sensitive environment, token, or diagnostic details in normal
  product chrome.
- Do not replace a mature project shell without explicit scope and regression
  checks.

## Pitfalls

- Treating the shell as decoration instead of product structure.
- Putting page titles, filters, or primary actions in both the app bar and page
  content.
- Building navigation from implementation modules instead of user destinations.
- Making desktop side navigation first and then shrinking it until mobile is
  unusable.
- Adding page-local gutters, widths, and action bars for each new route.
- Hiding unavailable functionality without route/service authorization.
- Using environment/build/status copy as prominent user-facing content.

## Examples

- Enterprise MEAL expanded layout: permanent left navigation drawer, top app
  bar with route title/status, page action lane, dashboard/list/form workspace,
  and compact footer status.
- Enterprise MEAL compact layout: modal navigation drawer, same route identity
  contract, stacked content workspace, and primary page actions visible before
  secondary filters.
- Viewflow workflow task page: shared shell owns the route title and back
  action; the workflow form renders inside the workspace using Viewflow form
  primitives.

## Verification

- Validate the relevant skillpack after adding this skill to a project.
- For Viewflow/Django projects, run `manage.py check` and focused template tests
  for routes affected by the shell.
- For frontend-heavy shells, run available build/tests and a browser check.
- Confirm at least one representative page uses the shared shell regions:
  navigation, top app bar, route identity, action lane, workspace, and footer.

## Output format

```markdown
## M3 Application Shell Check

- Users/work context:
- Navigation model:
- Adaptive behavior:
- Shell regions:
- Viewflow/frontend mapping:
- Token usage:
- Accessibility:
- State coverage:
- Tests/rendered evidence:
- Remaining shell risk:
```
