---
name: gepg-billing
description: Use this skill for NIMR billing system work involving GePG integration, invoices, control numbers, callbacks, receipts, reconciliation, and payment safety.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
  - python
requires_approval_for:
  - payment_logic_change
  - database_migration
  - production_config_change
  - destructive_command
activation:
  keywords:
    - gepg
    - billing
    - payment
    - callback
    - reconciliation
  required_files:
    - pyproject.toml
  optional_tools:
    - pytest
    - python
category: domain
scope: bundled
status: stable
visibility: public
bucket: domain
---
# GePG Billing

## Purpose

Guide safe changes to Django billing and GePG payment integration workflows.

## When to use this skill

Use for Django billing models, control number generation, payment callbacks, idempotency, reconciliation, cancellations, invoices, receipts, Celery tasks, Redis/RabbitMQ, callback logs, and duplicate payment prevention.

## When not to use this skill

Do not use for non-payment Django features, Invenio-specific work, or research writing.

## Core concepts

- Payment callbacks must be idempotent.
- External provider payloads must be logged safely and validated before state changes.
- Reconciliation must tolerate retries, duplicates, and out-of-order events.

## Standard workflow

1. Read billing memory and existing payment flow.
2. Identify state transitions and idempotency keys.
3. Check callback validation, duplicate handling, and transaction boundaries.
4. Add tests for duplicate callbacks and failure modes.
5. Document operational and reconciliation risks.

## Safety rules

- Do not change payment state transitions without tests.
- Do not print or commit payment secrets.
- Do not run destructive payment or reconciliation commands without approval.

## Required checks

- Test duplicate callback handling.
- Test failed or partial provider payloads.
- Test invoice, receipt, and cancellation state transitions where affected.

## Output format

Return summary, changed files, tests run, payment risks, and approval requirements.

## Examples

- Review duplicate callback handling for idempotency.
- Check reconciliation behavior for partial provider failures.

## Quick Reference

- Payment callbacks must be idempotent and auditable.
- Validate provider payloads before state changes.
- Add tests for duplicate, delayed, partial, and failed callbacks.

## Pitfalls

- Do not disable verification to make tests pass.
- Do not log or expose payment secrets.
- Do not change payment state transitions without regression tests.

## Verification

- Run billing callback and reconciliation tests.
- Check transaction boundaries and idempotency keys.
- Document approval requirements for payment logic changes.

## Examples

- Fix duplicate callback handling by enforcing idempotent transaction updates.
- Review reconciliation mismatch handling before changing settlement logic.
