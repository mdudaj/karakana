---
name: django-debugging
description: Use this skill for general Django debugging across views, models, migrations, forms, serializers, Celery, tests, settings, performance, pagination, and logging.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
  - python
requires_approval_for:
  - database_migration
  - production_config_change
  - destructive_command
activation:
  keywords:
    - django
    - migration
    - view
    - model
    - celery
  required_files:
    - manage.py
  optional_tools:
    - pytest
    - python
category: development
scope: bundled
---
# Django Debugging

## Purpose

Guide focused diagnosis and repair of Django application issues.

## When to use this skill

Use for Django views, models, migrations, forms, serializers, Celery tasks, tests, settings, performance, pagination, and logging.

## When not to use this skill

Do not use for payment-specific GePG logic when `gepg-billing` is more precise, or for Invenio-specific behavior when `invenio-framework` applies.

## Core concepts

- Reproduce the failing behavior before editing when possible.
- Follow Django ownership boundaries across settings, URLs, views, serializers, forms, models, and tests.
- Migrations and production settings require extra review.

## Standard workflow

1. Identify the failing route, task, model, or test.
2. Inspect the narrowest owning code path.
3. Add or adjust a focused regression test.
4. Apply a small patch.
5. Run relevant tests and document remaining risk.

## Safety rules

- Do not run destructive database commands.
- Do not modify production settings or secrets without approval.
- Treat migrations as review-required.

## Required checks

- Run focused Django tests.
- Check migrations when models change.
- Check logging and error handling for user-facing failures.

## Output format

Return root cause, fix summary, tests run, and risks.

## Quick Reference

- Reproduce or localize the failure before editing.
- Follow Django boundaries: settings, URLs, views, serializers/forms, models, tasks, and tests.
- Treat migrations and production settings as review-required.

## Pitfalls

- Do not run destructive database commands.
- Do not paper over exceptions without understanding user-visible behavior.
- Do not edit production settings or secrets without approval.

## Verification

- Run focused Django tests for the changed path.
- Check migrations if models changed.
- Check logs/error handling for user-facing failures.

## Examples

- Debug a pagination regression by testing query parameters and expected page metadata.
- Repair a Celery task failure by isolating retry, idempotency, and logging behavior.
