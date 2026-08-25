# UX Skill Router Matrix

Use this matrix to select the smallest useful skill sequence for interface work.

## Route by task signal

| User/task signal | Primary skill | Common supporting skills | Verification |
|---|---|---|---|
| Screenshot critique, “doesn’t look right”, layout polish | `visual-design-review` | `material-hcd-interface`, `material-component-spec`, `design-token-system` | `design-qa-playwright` |
| Page hierarchy, workflow cockpit, dashboard, landing, help index | `material-hcd-interface` | `visual-design-review`, `ux-writing`, `interaction-state-design` | `design-qa-playwright` |
| Repeated cards, tabs, filters, chips, empty states, action rows | `material-component-spec` | `design-token-system`, `interaction-state-design`, `accessibility-wcag-audit` | `design-qa-playwright` |
| Shared spacing, color, type, radius, elevation, density, theme | `design-token-system` | `design-system-governance`, `accessibility-wcag-audit` | visual/browser checks |
| Cross-page consistency, reusable rule, design-system protocol | `design-system-governance` | `material-component-spec`, `design-token-system`, `visual-design-review` | affected-page evidence |
| Viewflow shell/page/template/cards/tabs/forms surface | `viewflow-material-ui` | `material-hcd-interface`, `design-system-governance` | browser smoke/screenshot |
| Viewflow fields, AJAX select, date/time picker, dependent fields | `viewflow-form-controls` | `ux-writing`, `interaction-state-design`, `accessibility-wcag-audit` | Playwright interaction |
| Empty/loading/error/permission/stale/disabled/success state | `interaction-state-design` | `ux-writing`, `accessibility-wcag-audit`, `material-component-spec` | state assertions |
| Labels, buttons, helper text, error copy, empty-state copy | `ux-writing` | `accessibility-wcag-audit`, `material-hcd-interface` | copy assertions when critical |
| WCAG, keyboard, focus, contrast, ARIA, labels | `accessibility-wcag-audit` | relevant component/form/state skill | axe/manual evidence |
| E2E UI proof, screenshot evidence, visual regression | `design-qa-playwright` | specialist skill that defines expected UI | browser artifacts |

## Route by deliverable

### Plan only

Use the primary specialist skill plus this router output. Do not load browser QA
unless the plan must define verification.

### Implement UI

Use the primary specialist skill, any necessary supporting skill, then
`design-qa-playwright` for rendered verification if the page/component is
important or the user requested end-to-end review.

### Review after screenshot

Use `visual-design-review` first. It should classify issues by severity and
route systemic fixes to the right specialist skill.

### Harden existing UI

Use `design-system-governance` if the issue repeats across pages. Use
`design-qa-playwright` to ensure the regression has a browser-visible check.

## Minimality rule

Prefer one primary skill and one to three support skills. Loading five or more
UX skills is only justified for a major design-system slice, accessibility gate,
or release hardening pass.

## Delivery rule

For implemented UX work, the final summary should report:

- requirement/look-and-feel evidence used;
- specialist skills applied;
- affected pages/components;
- rendered verification performed;
- remaining UX risks;
- next recommended UX task.

