# Viewflow Frontend Patterns

Frontend changes can alter workflow correctness.

## Forms

- Check field requirements, validation, initial values, hidden fields, and save behavior.
- Ensure form validation matches backend transition rules.

## Views

- Confirm views enforce permissions and ownership, not only template visibility.
- Check success URLs, error handling, and task completion behavior.

## Viewsets

- Review task actions, list/detail views, URL wiring, permission hooks, and dashboard integration.

## Templates

- Check visible actions, disabled actions, state labels, error messages, and audit information.

## Frontend Actions

- Verify buttons map to valid transitions.
- Prevent unauthorized users from triggering hidden or forged actions.

## Dashboard Navigation

- Check task lists, process lists, badges, filters, and role-specific navigation.

## User-Facing Task Actions

- Test approval, rejection, reassignment, cancellation, and completion paths from the UI.
