---
name: invenio-ils-customization
description: Use this skill when customizing NHRILS or any Invenio-App-ILS catalogue, library circulation, patron, document, series, item, e-item, vocabulary, search, facet, statistics, notification, or backoffice workflow. Use before designing a catalogue shell, changing ILS JSON schemas, REST endpoints, permissions, OpenSearch mappings, record serializers, seeded library data, or InvenioILS UI/theme assets.
version: 0.1.0
risk_level: high
category: domain
scope: bundled
status: experimental
visibility: public
bucket: domain
activation:
  keywords:
    - invenio-ils
    - invenio app ils
    - nhrils
    - catalogue
    - catalog
    - circulation
    - patron
    - library item
    - e-item
    - library backoffice
    - library search
  required_files:
    - invenio_app_ils/config.py
    - setup.cfg
  optional_tools:
    - grep
    - git
    - pytest
allowed_tools:
  - read_file
  - grep
  - code_search
  - web_search
  - run_tests
  - python
requires_approval_for:
  - database_migration
  - production_config_change
  - authentication_change
  - permission_change
  - opensearch_index_change
  - index_rebuild
  - circulation_policy_change
  - patron_data_import
  - destructive_command
---
# InvenioILS Customization

## Purpose

Guide NHRILS and Invenio-App-ILS work from the ILS domain model and extension points before changing catalogue UX, records, search, circulation, patrons, or deployment behavior.

## When to use this skill

Use for:

- public catalogue shell, search, detail pages, facets, sort, empty states, and help pages;
- librarian backoffice, catalogue management, item/e-item workflows, document requests, loans, acquisitions, providers, and statistics;
- JSON schema, Marshmallow loader, serializer, REST endpoint, PID, vocabulary, relation, mapping, indexer, or Celery changes;
- ILS permissions, patron ownership, backoffice roles, file access, notification, or mail behavior;
- seed data or data migration plans for documents, items, locations, internal locations, patrons, and vocabularies.

Use `invenio-framework` alongside this skill for general Invenio extension, Flask, database, OpenSearch, service, and deployment patterns. Use `design-system-governance` and `system-design-thinking` before UX implementation.

## When not to use this skill

Do not use for unrelated Django, Power Platform, billing, or general research-writing work. Do not use it as a replacement for `invenio-framework` when the work is general Invenio infrastructure with no ILS-specific catalogue, circulation, patron, or backoffice concern.

## Quick Reference

Before editing, inspect:

- `setup.cfg` entry points: apps, API apps, blueprints, config modules, schemas, mappings, PID minters/fetchers, access actions, Celery tasks, webpack bundle;
- `invenio_app_ils/config.py`: `RECORDS_REST_ENDPOINTS`, sort options, facets, `ILS_VOCABULARIES`, file permissions, cover URL builder, metadata extensions, stats, mail, feature flags, site theme;
- domain modules: `documents`, `series`, `literature`, `items`, `eitems`, `locations`, `internal_locations`, `patrons`, `circulation`, `document_requests`, `acquisition`, `providers`, `vocabularies`, `stats`, `notifications`;
- schemas/loaders/mappings/indexers for the affected record type;
- permissions/search filters before exposing any record-level data;
- tests under `tests/api/**` and fixture data under `tests/data/**`.

## Core concepts

- Patrons search/browse the aggregated `literature` view, while librarians manage `documents` and `series` in backoffice.
- `Document` is the shared bibliographic record; `Item` is a physical copy; `EItem` is a digital instance; locations and internal locations model library placement.
- Catalogue UX changes usually depend on `RECORDS_REST_ENDPOINTS`, `RECORDS_REST_SORT_OPTIONS`, `RECORDS_REST_FACETS`, serializers, search classes, and OpenSearch mappings.
- Circulation behavior is policy-sensitive. Treat `CIRCULATION_LOAN_TRANSITIONS`, self-checkout, patron ownership, loan extension, overdue notices, and document requests as workflow changes.
- Public record visibility is controlled by permissions plus search filters, not by hiding UI controls.
- Invenio discovers behavior through Python entry points; changes can be invisible if entry points, config loading, or package data are missed.

## Standard workflow

1. State the user-facing library workflow and the affected ILS entities.
2. Read the official InvenioILS reference or configuration page relevant to the change.
3. Inspect local source for entry points, config, record classes, schemas/loaders, serializers, mappings, indexers, permissions, and tests.
4. Decide whether the change is catalogue UI only, configuration-only, schema/index, workflow, permission, or data migration.
5. For UX work, define reusable design-system rules and avoid page-local styling unless the repository already uses that pattern.
6. For record/search changes, update schema, loader, serializer, mapping, facets/sort, fixtures, and tests together.
7. For permission, authentication, circulation, migration, or indexing changes, stop for approval and document rollout/reindex impact.
8. Run focused tests or record why the local environment cannot run them.

## Safety rules

- Do not change authentication, permissions, circulation policy, migrations, production config, OpenSearch mappings, or data imports without explicit approval.
- Do not expose patron personal data through public catalogue endpoints or facets.
- Do not assume every bibliographic need requires a schema change; prefer vocabularies or metadata extensions when that matches InvenioILS patterns.
- Do not assume a React/Vite frontend exists in this repo. Verify asset, template, and webpack ownership first.
- Do not run index rebuilds, migration commands, or destructive data commands without approval.

## Required checks

- Identify the affected ILS entity and public/backoffice surface.
- Inspect the local entry point/config/schema/mapping/permission path before editing.
- Check official InvenioILS or Invenio documentation for unstable or framework-owned behavior.
- Record approval needs for permission, authentication, circulation, migration, production config, data import, and OpenSearch index changes.
- Run focused tests or document why they cannot run.

## Pitfalls

- Updating a visible catalogue field without updating search mappings/facets leaves the UI and index inconsistent.
- Treating `literature`, `documents`, and `series` as interchangeable can break public search or backoffice editing.
- Changing patron behavior is constrained by InvenioILS; official docs note patron customization is limited.
- Adding route-level UI access without permission factories or search filters can leak records.
- Changing mail/notification defaults can silently fail when mail is suppressed or sender configuration is incomplete.

## Verification

- Validate skills when this skill changes: `karakana skill validate skills/invenio-ils-customization`.
- Validate NHRILS skillpack after registration: `karakana skillpack validate nhrils`.
- For code changes, run focused tests for the touched module, then broader `pytest` when feasible.
- For search or facet changes, verify mapping impact and document whether reindexing is required.
- For UX shell changes, verify desktop/mobile catalogue states: unauthenticated search, no results, results list, record detail, restricted item/e-item, signed-in patron, and librarian/backoffice path.

## Output format

Return:

- selected InvenioILS entities and layers;
- source files and official references inspected;
- approval gates triggered;
- implementation or design steps;
- verification commands/results;
- indexing, migration, permission, and deployment risks.

## Examples

- Plan a NIMR-branded catalogue shell by inspecting `literature` search, facets, theme assets, templates, and CERN catalogue behavior before writing UI.
- Review adding a subject vocabulary by checking vocabulary source, schema usage, loader validation, facet configuration, fixtures, and tests.
- Diagnose why a patron cannot request a loan by checking authentication, patron record, `CIRCULATION_LOAN_TRANSITIONS`, permission factories, and document/item circulation state.
