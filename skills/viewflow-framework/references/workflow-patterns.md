# Viewflow Workflow Patterns

Use this reference when reviewing workflow structure.

## Start Nodes

- Confirm who can start the workflow.
- Confirm required business data exists before process creation.
- Check duplicate-start behavior.

## Human Tasks

- Identify actor, assignment, permissions, form, validation, and completion rules.
- Check whether task visibility matches ownership and role rules.

## Automated Tasks

- Confirm deterministic inputs and outputs.
- Check retry behavior, idempotency, error handling, and logging.

## Approvals

- Identify approval authority, substitute approvers, rejection paths, auditability, and notifications.
- Approval workflows require permission and assignment review.

## Branching

- Verify each branch condition is explicit and tested.
- Avoid hiding branch decisions only in UI code.

## Joins

- Confirm all required parallel work completes before the join.
- Test partial completion and cancellation behavior.

## Cancellation

- Define who can cancel, when cancellation is allowed, what business data changes, and what audit trail remains.

## Completion

- Define the final workflow state and business record effect.
- Test completed state visibility and immutability where required.

## Error States

- Document failed automated tasks, invalid submissions, and recovery paths.

## Rework Loops

- Ensure rejected work returns to the correct actor or queue.
- Test repeated rework and final approval.
