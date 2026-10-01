# Billing Known Issues

- The `../billing` checkout was absent on 2026-10-01; project code and tests
  were not inspected for this memory restoration.
- Payment callback idempotency, retry handling, reconciliation and cancellation
  behavior remain task-specific verification targets, not known defects.
