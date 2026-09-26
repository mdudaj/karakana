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

### Control-level reflow and focus regressions

For layout bugs, pair page-width smoke checks with assertions on the affected
search fields, selects, action buttons and context indicators. Check 320 CSS
pixels where reflow applies, a representative compact width and the reported
laptop viewport, with relevant sidebar states. Scroll vertically to the control,
then inspect its bounds against both the viewport and overflow-clipping ancestors;
verify it is not only measurable but reachable (for example, a trial click or
keyboard activation). Opening an unrelated control must not horizontally scroll
the whole work surface to hide the original problem.

Explicitly open details/popups before checking their contents. Closed `details`
descendants can produce misleading raw geometry; test only the intended visible
state. Permit contained two-dimensional scrolling only for documented exceptions
such as data tables, not all descendants of a page.

Check icon centring using the glyph/text region, not only the circle dimensions.
Verify that identity/metadata text has usable width; controls fitting inside a
row must not count as a pass when adjacent text collapses to single characters.
Check row balance and the distance to actionable work in rendered evidence;
do not encode a universal maximum page height. Include populated and empty data,
long identifiers and missing scope values where relevant.

For disclosures, test Enter/Space, Tab into content, Escape and focus restoration,
outside focus/click, and repeated navigation/cache restoration. Match assertions
to the declared disclosure or menu pattern: the two have different keyboard
contracts. A test which observes a hidden focused link must fail.

Keep diagnostic fixtures in isolated test data. Record the red-to-green result
when correcting an existing defect and retain screenshots for visual review.
These checks do not certify screen-reader support or complete WCAG conformance.

### Evidence fields

Record:

- command run;
- route(s);
- viewport(s);
- user role/context/data fixture;
- assertions covered;
- screenshot/trace/report paths;
- pass/fail result;
- unresolved visual or accessibility risk.
