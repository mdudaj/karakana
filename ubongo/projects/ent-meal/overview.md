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
release state. **23 October2026:** the completed Windows work and portable Ubuntu
checkpoint are squash merged through
[ent-meal PR99](https://github.com/mdudaj/ent-meal/pull/99) at `80aa22b`.
Read `docs/deployment/ubuntu-continuation-2026-10-23.md` from fetched application
main before following an older Linux runtime handoff. It includes the current
organisation/settings artifacts, exact operator receipts, CI/CD direction and
pending portfolio work. This documentation integration does not require a new
runtime image. Server-side UAT health and persistence/443 configuration passed;
browser ingress and actual post-session/reboot/failure recovery remain unverified.
The GitHub egress probe is prepared but unrun; legacy NIMR deployment remains
manually disabled. Next independent Ubuntu task is the isolated hosted-CI slice;
CD activation still needs site egress, deployment identity and guarded upgrades.

Earlier checkpoint (historical): FR02 is squash merged at `16ee712`; live preview checks remain
user-deferred until VPN is available. Local v0.3 clarification/name corrections
are a separate review branch and do not imply integration or acceptance.

## Current Client Documentation Decisions

On 16 November 2026 the user reaffirmed LDAP as the agreed institutional
authentication method. Do not ask reviewers to select or reconfirm it. Our
implementation/UAT team performs configuration and readiness tests, reports
failures or unresolved inputs, and uses its final configuration assessment to
inform the documents. Reuse the latest assessment to distinguish completed work
from actual pending work; do not replace it with generic external confirmations.
UAT records the actual LDAP service configuration, application account bindings,
TLS and session policy; MFA applicability/enforcement remain separate open inputs.
Carry settled decisions into documents as facts. Ask for resolution only of
missing or changed inputs, and distinguish checking test readiness from reopening
a decision. Use descriptive purpose/scope prose and direct execution instructions.
See application `docs/delivery/2026-11-15-release1-client-uat.md` for authority,
scope, evidence and the current UAT issue; load the latest handoff for delivery
state. These documentation decisions do not claim deployed LDAP or MFA evidence.

The agreed UAT workbook uses three sheets: Setup and Assessment, Test Results,
and Retests. Maintain changing configuration findings in the existing setup
assessment area; keep stable testing instructions in the guide. Combine initial
observations, evidence and issue follow-up per case, and preserve initial results
when recording later retests. Verify populated screen and print examples before
issuing revisions; fewer sheets alone do not establish clarity.

Prefill known UAT configuration and completed assessment facts from the actual
recorded evidence, with dates and scope. A qualified candidate is not evidence
of activation. Do not turn blank workbook metadata into configuration issues.
Retain client content only when it helps preparation, testing, evidence,
follow-up or acceptance; keep exhaustive research and engineering controls in
internal records. Remove duplicate prompts instead of asking reviewers to
re-enter known facts or reconfirm settled choices.

## Original Scaffold Boundary

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
