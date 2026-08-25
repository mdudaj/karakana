# WCAG UI Audit Reference

Use this reference for practical accessibility planning and review.

## Default conformance profile

Default new web UI work to WCAG 2.2 AA unless the project declares another
profile. WCAG 2.2 is additive over WCAG 2.1 for most practical purposes and
adds important UI criteria around focus, dragging, target size, help,
redundant entry, and authentication.

## Manual and automated evidence

Automated tools are necessary but not sufficient.

Use automated checks for:

- missing labels;
- invalid ARIA;
- many color contrast failures;
- duplicate IDs;
- landmark/heading issues;
- some keyboard/focus issues.

Use manual checks for:

- whether the interaction sequence matches the user’s task;
- whether the accessible name is meaningful;
- whether focus moves predictably across a complete flow;
- whether custom controls behave like their announced role;
- whether copy helps the user recover from errors;
- whether hidden/revealed content is announced at the right time.

## Core checklist

### Structure

- One useful `h1` per page or equivalent route title.
- Headings form a meaningful outline.
- Landmarks identify navigation, main content, search, complementary panels,
  and footer where present.
- Tables use table semantics when users compare rows/columns.
- Lists use list semantics when order/grouping matters.

### Controls

- Buttons perform actions; links navigate.
- Icon-only controls have accessible names.
- Disabled controls have an understandable reason when the user needs one.
- Destructive actions include accessible confirmation and recovery where
  possible.
- Target size and spacing support pointer use in the actual work environment.

### Forms

- Every control has a label or equivalent accessible name.
- Related fields are grouped.
- Required fields are clear.
- Instructions appear before or near the relevant field.
- Validation errors identify the field and the correction needed.
- Submitted values are preserved after validation failure.
- Long forms are split into logical steps with progress indication.

### Focus and keyboard

- Tab order follows visual/task order.
- Focus indicator is visible and not obscured.
- No keyboard trap exists.
- Dialogs/sheets trap focus while open and restore it on close.
- Menus, tabs, comboboxes, date pickers, and grids follow expected keyboard
  behavior.
- Escape closes transient popups when safe.

### Visual accessibility

- Text contrast meets the project target.
- Meaning is not conveyed by color alone.
- Focus/hover/selected/error states are distinguishable.
- Text can resize without clipping key content.
- Motion is avoidable/reduced where needed.
- Dense operational screens remain readable under real lighting/device
  conditions.

### Dynamic state

- Loading and async completion states are perceivable.
- Status messages are available to assistive technology when they update the
  user on success, progress, or errors.
- Filtered-empty and no-results states explain the state and recovery path.
- Permission-denied states explain what the user can do next without exposing
  unauthorized data.

## Combobox/autocomplete checklist

- The input has an accessible name.
- The popup behavior is predictable and keyboard-accessible.
- Down/Up arrows, Enter, Escape, and printable characters behave as expected.
- The selected/active option is conveyed programmatically.
- Suggestions remain scoped to authorized records.
- No-results and loading states are visible and announced where appropriate.
- Submitted IDs are revalidated server-side.

## Severity model

| Severity | Meaning | Examples |
| --- | --- | --- |
| P0 | Blocks task or excludes a user group | Keyboard trap, unlabeled critical field |
| P1 | Serious task failure or high error risk | Autocomplete unusable by keyboard |
| P2 | Degraded access or inefficient recovery | Weak error message, poor focus order |
| P3 | Polish/future improvement | Minor copy refinement |

## Verification record

For each audited screen, record:

- URL/route and state tested;
- viewport/device class;
- user role/context;
- automated tool and result;
- manual keyboard path tested;
- custom controls tested;
- unresolved findings and severity;
- screenshots or trace artifacts where useful.
