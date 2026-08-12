# LIMS Overview

LIMS is the NIMR single-lab laboratory information management system project in
`../lims`.

The current phase is a phase-1 single-lab LIMS. Do not implement SaaS
multi-tenancy, tenant routing, entitlements, billing, or deployment stamps in
this phase. Future Mtafiti integration is an extension concern, not the first
implementation boundary.

## Current Intent

- Support regulated laboratory operations for specimen accession, QC, storage,
  downstream processing, discrepancies, record control, and reconstruction.
- Use Django, Viewflow OSS, PostgreSQL, Redis, Celery, django-guardian, and
  Viewflow/django-material-aligned operator surfaces.
- Keep governed runtime evidence separate from typed LIMS domain projections.
- Preserve attributable actors, timestamps, package/workflow context, raw and
  normalized submissions, validation results, operational events, and
  reconstruction evidence.

## Repository

- Path: `../lims`
- Workspace: `nimr`
- Skillpack: `lims`
- Primary local instructions: `../lims/AGENTS.md`
- Documentation index: `../lims/docs/README.md`

## First Files To Inspect

- `AGENTS.md`
- `docs/CONTEXT.md`
- `docs/AGENT_HARNESS.md`
- `docs/HARNESS_ENGINEERING.md`
- `docs/planning/PHASE_1_RESEARCH_PLAN.md`
- `docs/REQUIREMENTS.md`
- `docs/DOMAIN_MODEL.md`
- `docs/WORKFLOWS.md`
- `docs/DATA_DICTIONARIES.md`
- `docs/OPERATION_FORM_ENGINE.md`
- `docs/DOCS_MAINTENANCE.md`
- `docs/planning/OPERATION_ENGINE_REALIGNMENT_PLAN.md`
- `docs/ARCHITECTURE.md`
- `docs/VERIFICATION.md`
- `docs/PROGRESS.md`
- `feature_list.json`

## Current Tracker State

As checked on 2026-08-12, `feature_list.json` has 84 items:

- 83 `done`
- 1 `deferred`: `lims-reconstruction-package-001`

## Safety

- Work on one vertical slice at a time.
- Preserve phase-1 single-lab scope.
- Do not touch secrets or `.env` files.
- Do not push, deploy, merge, or run destructive commands without explicit
  approval.
- Authentication, permission, migration, workflow-state, and production-config
  changes require explicit approval and focused verification.
- Browser-visible UI must follow the LIMS Viewflow/MDC/django-material design
  system and existing shared tokens/components.
