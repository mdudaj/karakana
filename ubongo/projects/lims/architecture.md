# LIMS Architecture

LIMS is currently a runnable Django/Viewflow application, not just a planning
repository.

## Implemented App Boundaries

- `config/` - Django settings, URL routing, ASGI/WSGI, Celery, email backend.
- `apps/users/` - custom email user model, role catalog, invitations, password
  self-service, dashboard read model helpers, and bootstrap superuser command.
- `apps/shell/` - Viewflow site shell, dashboard route, pagination, titlecase,
  static authenticated shell behavior.
- `apps/reference/` - lab/study/site context, address reference models,
  Tanzania address sync/import services, Celery task, and configuration UX.
- `apps/operations/` - governed operation definitions, drafts, designer,
  workflow nodes, compiled artifacts, published-version immutability, and
  publication.
- `apps/runtime/` - Viewflow-backed operation runner, operation/step runs,
  submissions, field responses, validation results, ingest decisions,
  projection-failure review, lookups, and worklist helpers.
- `apps/storage/` - configurable storage topology, validation, occupancy,
  reservations, forms, and Viewflow shell pages.
- `apps/specimens/` - specimen accession, batch intake, QC/storage projection,
  downstream processing, downstream batches, discrepancies, corrections,
  record-state transitions, reconstruction exports, archives, and signatures.

## Architecture Position

- Operation definitions publish immutable operation versions.
- Viewflow owns process/task lifecycle through a stable dynamic adapter.
- Runtime submissions preserve evidence before domain projection.
- Domain services project accepted evidence into typed LIMS records.
- Projection failures are reviewable records, not silent mutations.
- Reconstruction is a read-only deterministic bundle over governed source
  records; archive/signature records are explicit artifacts.

## Local Runtime

The documented preview path uses Docker Compose PostgreSQL and Redis:

- PostgreSQL: `127.0.0.1:55433`
- Redis: `127.0.0.1:16380`
- Django dev server: `127.0.0.1:8000`

Direct SQLite fallback is not a full test path because at least one migration
uses PostgreSQL-specific SQL.

## UI Direction

Authenticated UX uses the Viewflow shell with LIMS-owned templates and shared
tokens/components under `static/lims/ui/`. Browser-visible workflow and
configuration surfaces should start from Viewflow/MDC/django-material anatomy
before local extensions.
