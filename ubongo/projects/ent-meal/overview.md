# Sustainability Monitoring and Reporting Platform Overview

Sustainability Monitoring and Reporting Platform is the planned Microsoft-aligned, Django/Viewflow-based Monitoring, Evaluation, Accountability, and Learning platform for CRDB Sustainable Finance Unit.

The repository is `/home/jmduda/KodeX/ent-meal`.

The platform replaces the TACATDP-specific Power Pages proof of concept as the long-term product direction. TACATDP remains the first reference configuration, but the platform must support multiple programmes, schemes, products, grants, guarantees, insurance-linked initiatives, ESG initiatives, and operational workstreams without hard-coding each one into software.

## Naming and current delivery

The approved public name is **Sustainability Monitoring and Reporting Platform**.
Use **Sustainability Reporting** for compact navigation. The requirements baseline
and platform overview already clarified this name; do not reopen it or restore the
obsolete name from historical records. `ent-meal` remains the technical project ID.
See `docs/ux/product-naming.md` in the application repository.

Load the latest handoff and `docs/delivery/first-release-milestones.md` for current
release state. FR02 is squash merged at `16ee712`; live preview checks remain
user-deferred until VPN is available. Local v0.3 clarification/name corrections
are a separate review branch and do not imply integration or acceptance.

## Original scaffold boundary

Slice 1 establishes:

- Django project scaffold.
- Viewflow application shell.
- local username/password bootstrap authentication.
- Material 3-inspired side navigation, top bar, content area, and footer.
- PostgreSQL, Redis, and Celery infrastructure contract.
- XLSForm/XForm form-runtime boundary.
- Microsoft Entra and Graph integration boundary as future configuration, not active authentication yet.

## Inspect first

- `/home/jmduda/KodeX/ent-meal/README.md`
- `/home/jmduda/KodeX/ent-meal/KARAKANA.md`
- `/home/jmduda/KodeX/ent-meal/AGENTS.md`
- `/home/jmduda/KodeX/ent-meal/docs/adr/`
- `/home/jmduda/KodeX/karakana/ubongo/projects/crdb-mel/django-viewflow-pivot-research.md`
- `/home/jmduda/KodeX/karakana/ubongo/projects/crdb-mel/ent-meal-bootstrap-plan.md`

## Operating rule

Do not copy Power Pages prototype constraints into Sustainability Monitoring and Reporting Platform unless they are explicitly part of the transitional import path. Use the Power Pages work as domain evidence and a migration source, not as the future architecture.

Before resuming non-trivial Sustainability Monitoring and Reporting Platform UI/UX work, update the Karakana harness context first: fetch/pull the Karakana repository, check whether UX skills or skillpacks changed, then load the latest `ent-meal` handoff and apply the active `ent-meal` skillpack. This prevents stale UI guidance when Material, Viewflow, HCD, or UX-writing skills have been updated upstream.
