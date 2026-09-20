# Material 3 and Viewflow application shell synthesis

This reference records the evidence basis for the `m3-application-shell` skill.
Use it to plan or audit application shells before implementation.

## Source basis

- Material Design 3 foundations: layout, adaptive design, color roles,
  typography, elevation, interaction states, and navigation components.
- Material Web: web components and M3 implementation direction for buttons,
  lists, navigation tabs, text fields, chips, icons, progress, and related
  controls.
- Android adaptive layout guidance: compact, medium, and expanded layout
  classes; navigation bar/rail/drawer selection; canonical layouts.
- Viewflow frontend: Material/Viewflow templates, `vf-*` layout classes, form
  rendering, workflow task pages, and Django template extension patterns.
- WCAG 2.2: keyboard access, focus visibility, labels, target size, status and
  error identification, contrast, and predictable behavior.
- GOV.UK service design and Nielsen Norman Group heuristics: task focus,
  plain-language navigation, visibility of system status, consistency, error
  prevention, recognition over recall, and minimalist but sufficient
  information.

## Strategic principles for an M3 shell agent

1. **Separate shell from page content.** The shell owns brand, navigation, route
   identity, global actions, workspace boundaries, and footer/status. Pages
   provide content and contextual actions only.
2. **Design by user destinations.** Navigation reflects user goals and stable
   product areas, not database tables or implementation modules.
3. **Use adaptive navigation deliberately.** Choose modal drawer, navigation
   rail, standard drawer, or permanent drawer by device class and task density.
4. **Keep action scope explicit.** Global actions belong in the app bar; page
   actions in the page action lane; section actions in section headers; row
   actions on rows.
5. **Use tokens for shell geometry.** Drawer width, rail width, app-bar height,
   gutters, spacing, surface colors, typography, active states, elevation,
   focus, and density must be tokenized.
6. **Use Viewflow as the implementation substrate when present.** Extend
   Viewflow templates and form/layout primitives before creating a parallel
   shell.
7. **Make states first-class.** Loading, no-access, permission denied, stale
   data, offline/sync, active route, collapsed drawer, and responsive states
   must be visible and accessible.
8. **Avoid implementation language in product chrome.** Navigation and route
   headers should use user-facing terms, not delivery/runtime vocabulary.
9. **Verify rendered structure.** Tests should prove pages share shell regions
   and do not duplicate headers, action lanes, or nav markup.

## Recommended skill catalogue shape

Use a layered catalogue rather than one overloaded UX skill:

```text
ux-skill-router
└── hcd-ui-ux-delivery-loop
    ├── m3-application-shell
    ├── material-hcd-interface
    ├── material-component-spec
    ├── design-token-system
    ├── viewflow-material-ui
    ├── viewflow-form-controls
    ├── interaction-state-design
    ├── ux-writing
    ├── accessibility-wcag-audit
    └── design-qa-playwright
```

Use `m3-application-shell` when the problem is the product frame. Use
`material-hcd-interface` when the problem is the content hierarchy inside the
workspace. Use `viewflow-material-ui` when implementing the shell/page
contracts in a Django/Viewflow project.

## Standard shell regions

| Region | Owned by | Notes |
|---|---|---|
| Brand/product identity | Shell | Logo, product name, organization context. |
| Navigation destinations | Shell | Grouped by user task, not implementation module. |
| Top app bar | Shell | Route title, subtitle/status, global actions, profile. |
| Page action lane | Shell/page contract | Actions scoped to the current route. |
| Workspace | Page | Dashboard, list, form, detail, or workflow content. |
| Footer/status | Shell | Only user-relevant sync/support/copyright/status. |
| Skip/focus landmarks | Shell | Required for keyboard and assistive technology. |

## Viewflow mapping checklist

- Does the page extend the shared Viewflow base template?
- Is route identity passed through context/template blocks?
- Are forms rendered using Viewflow layout/form primitives?
- Are workflow task states visible in the shared header/workspace pattern?
- Are shell CSS classes shared rather than copied into each page?
- Are route tests checking expected titles, actions, and access state?

## Verification examples

- `rg` confirms no page-local duplicate app shell wrappers in templates.
- Django tests confirm key routes use the shared shell template.
- Browser checks confirm active nav state, page title, action lane, and
  responsive drawer/rail behavior.
- Accessibility checks confirm landmarks, labels, focus-visible, and keyboard
  reachability.
