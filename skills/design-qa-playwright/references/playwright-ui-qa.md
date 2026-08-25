# Playwright UI QA Reference

Use this reference when planning or reviewing browser verification for UI work.

## Test layers

| Layer | Use | Preferred checks |
| --- | --- | --- |
| Render smoke | Route loads and core text/actions exist | headings, nav, page actions |
| Interaction | User can complete a flow | role/label locators, auto-retrying assertions |
| Component contract | Reusable UI anatomy remains intact | classes, roles, slots, counts |
| State coverage | Non-happy states are usable | empty, filtered-empty, error, permission |
| Visual comparison | Layout/polish regression evidence | targeted screenshots |
| Accessibility | Common a11y issues | axe scan + keyboard/focus manual checks |
| Responsive | Breakpoint behavior | compact/medium/expanded viewports |

## Locator priority

Prefer:

1. `getByRole()` with accessible name;
2. `getByLabel()` for form controls;
3. `getByText()` for visible copy;
4. `getByAltText()` for meaningful images;
5. `getByTitle()` where title is the actual contract;
6. `getByTestId()` for stable internal contracts that users do not see.

Avoid CSS/XPath selectors unless there is no semantic alternative or the test
is intentionally asserting a component implementation contract.

## Screenshot policy

Use screenshots for visual regressions that DOM assertions cannot express well:

- spacing between major sections;
- component alignment;
- responsive layout;
- visual density;
- surface hierarchy;
- icon sizing and alignment.

Avoid broad screenshots when the page contains:

- timestamps;
- random/demo data;
- notifications;
- cursor/focus animation;
- external iframes/widgets;
- charts with nondeterministic rendering.

Stabilize by using seeded data, fixed viewport, deterministic environment,
project-specific screenshot stylesheet/masking, and controlled browser project.

## State coverage matrix

For a meaningful UI change, consider:

- default/populated;
- loading;
- empty;
- filtered-empty;
- no-results;
- validation error;
- system error;
- permission denied;
- disabled/readonly;
- stale data;
- success;
- queued/background;
- responsive compact/expanded.

Document why omitted states cannot occur or are covered elsewhere.

## Accessibility checks

Automated:

- axe scan for current page/state;
- role/name assertions for key controls;
- label assertions for fields;
- status/error text visibility.

Manual/browser:

- keyboard-only path;
- focus visibility and order;
- Escape behavior for dialogs/popups;
- focus restoration;
- screen-reader-sensitive custom controls where applicable.

## Delivery evidence format

Record:

- command run;
- route(s);
- viewport(s);
- user role/context/data fixture;
- assertions covered;
- screenshot/trace/report paths;
- pass/fail result;
- unresolved visual or accessibility risk.
