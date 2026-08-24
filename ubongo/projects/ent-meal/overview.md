# Enterprise MEAL Overview

Enterprise MEAL is the planned Microsoft-aligned, Django/Viewflow-based Monitoring, Evaluation, Accountability, and Learning platform for CRDB Sustainable Finance Unit.

The repository is `/home/jmduda/KodeX/ent-meal`.

The platform replaces the TACATDP-specific Power Pages proof of concept as the long-term product direction. TACATDP remains the first reference configuration, but the platform must support multiple programmes, schemes, products, grants, guarantees, insurance-linked initiatives, ESG initiatives, and operational workstreams without hard-coding each one into software.

## Current slice

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

Do not copy Power Pages prototype constraints into Enterprise MEAL unless they are explicitly part of the transitional import path. Use the Power Pages work as domain evidence and a migration source, not as the future architecture.
