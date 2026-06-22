# Viewflow Testing Checklist

Workflow behavior changes require tests.

## Required Test Areas

- Process starts successfully.
- Valid transition succeeds.
- Invalid transition fails.
- Permissions are enforced.
- Form validation is enforced.
- User assignment is enforced.
- Final state is reached.
- Completed state behaves correctly.
- Cancelled state behaves correctly where applicable.
- Rejection or rework path behaves correctly where applicable.

## Edge Cases

- Duplicate submissions.
- Unauthorized users.
- Missing business data.
- Active processes created before a workflow change.
- Failed automated tasks.
- Repeated rejection and resubmission.
