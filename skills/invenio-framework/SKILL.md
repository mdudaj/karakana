---
name: invenio-framework
description: Use this skill when working on Invenio Framework, InvenioRDM, NHRDM, custom fields, vocabularies, OAuth/SSO, OpenSearch, dashboards, permissions, records, deposits, or migrations.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
  - python
requires_approval_for:
  - database_migration
  - production_config_change
  - authentication_change
  - permission_change
  - index_rebuild
  - destructive_command
activation:
  keywords:
    - invenio
    - invenio-rdm
    - nhrdm
    - opensearch
    - custom fields
  required_files:
    - pyproject.toml
  optional_tools:
    - pytest
    - git
category: domain
scope: bundled
status: stable
visibility: public
bucket: domain
---
# Invenio Framework

## Purpose

Guide work across Invenio Framework, InvenioRDM, and NHRDM customization.

## When to use this skill

Use for Flask extension patterns, SQLAlchemy models, Alembic migrations, services/resources, records and drafts, custom fields, vocabularies, subjects, OAuth/SSO, OpenSearch indexing, dashboard customization, deposit forms, permissions, communities, requests, background jobs, and deployment checks.

## When not to use this skill

Do not use for unrelated Django billing, general academic writing, or infrastructure-only changes unless they directly affect an Invenio deployment.

## Core concepts

- Invenio behavior is often split across configuration, services, resources, records, schemas, forms, mappings, and indexers.
- Migrations, permissions, authentication, and index changes require explicit review.
- Repository code is the current source of truth when memory or references are stale.

## Standard workflow

1. Read project memory and deployment notes.
2. Locate extension, service, schema, configuration, and test ownership.
3. Make the smallest behavior-preserving change possible.
4. Add or update focused tests.
5. Document migration, indexing, permission, and deployment risks.

## Safety rules

- Do not change authentication, permissions, migrations, production config, or index mappings without explicit approval.
- Do not expose secrets.
- Do not run destructive database or index commands without approval.

## Required checks

- Run focused unit tests for changed behavior.
- Check migrations when models change.
- Check OpenSearch mappings when indexed fields change.
- Check permissions for records, drafts, communities, and requests.

## Output format

Return implementation summary, affected Invenio layers, tests run, approval requirements, and deployment/indexing risks.

## Examples

- Review a custom field loader change for schema, mapping, migration, and indexing impact.
- Triage OAuth invalid client errors without exposing secrets.

## Quick Reference

- Check configuration, services, resources, schemas, mappings, forms, permissions, and tests together.
- Treat authentication, permissions, migrations, production config, and index rebuilds as approval-required.
- Prefer repository code over stale memory.

## Pitfalls

- Do not update OpenSearch mappings without considering reindexing.
- Do not change permissions or authentication as a side effect.
- Do not assume Invenio behavior lives in one file.

## Verification

- Run focused tests for changed services, schemas, or resources.
- Check migrations and mappings for data/index changes.
- Document deployment, reindexing, and permission risks.

## Output format

Return summary, changed files, tests run, risks, and approval requirements.

## Examples

- Review custom field design for required schema, form, mapping, and test coverage.
- Diagnose OAuth invalid client errors by checking client ID, redirect URI, provider config, and secret handling.
