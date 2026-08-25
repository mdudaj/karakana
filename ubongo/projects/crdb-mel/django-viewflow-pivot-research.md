# Enterprise MEAL Django/Viewflow Architecture Pivot Research

Date: 2026-08-24

Status: initial research and planning artifact. This does not create the new repository and does not retire the current Power Pages demonstration path.

## Context

CRDB may provide a Docker-capable environment. That changes the long-term architecture option for the Sustainable Finance MEL Platform: the scalable product can move from Power Pages as the main runtime to a configurable Django platform while keeping Microsoft tenant integration where CRDB policy requires it.

Agreed product/repository naming:

- Platform name: `Enterprise MEAL`
- Repository name: `ent-meal`

The current Power Pages/Dataverse prototype remains useful for demonstration, baseline-import evidence, dashboard concepts, and lessons about CRDB permissions. The new architecture should compound that research rather than discard it.

## Evidence inspected

Local project memory:

- `ubongo/projects/crdb-mel/overview.md`
- `ubongo/projects/crdb-mel/architecture.md`
- `ubongo/projects/crdb-mel/decisions.md`
- `ubongo/projects/crdb-mel/known-issues.md`
- `.karakana/milestones/20260812-144227-milestone-09ee8f/next-milestone.md`

Reference repositories:

- `../lims/templates/viewflow/base_page.html`
- `../lims/templates/viewflow/includes/lims_site_menu.html`
- `../lims/apps/shell/site.py`
- `../lims/static/lims/ui/tokens.css`
- `../lims/static/lims/ui/authenticated.css`
- `../lims/config/settings.py`
- `../lims/docker-compose.dev.yml`
- `../lims/docs/adr/0006-viewflow-backed-dynamic-operation-runner.md`
- `../lims/docs/adr/0014-viewflow-mdc-operation-workspace-ux.md`
- `../lims/docs/adr/0027-authenticated-shell-navigation-information-architecture.md`
- `../stemgen-platform/templates/base.html`
- `../stemgen-platform/static/dissertation/ui/tokens.css`
- `../stemgen-platform/static/dissertation/ui/authenticated.css`
- `../stemgen-platform/config/settings.py`
- `../stemgen-platform/docker-compose.yml`
- `../stemgen-platform/docs/adr/0001-django-viewflow-platform.md`
- `../stemgen-platform/docs/adr/0002-postgres-redis-celery.md`
- `../stemgen-platform/docs/adr/0004-oss-viewflow-extension-strategy.md`

External references checked:

- Google Material Design 3: layout scaffolds, canonical layouts, state layers.
- Viewflow official documentation: Django business application library, BPMN workflow engine, code-first workflows, workflow state, tasks, permissions, and Viewflow frontend.
- Django official documentation: web-app authentication model and current task framework context.
- Celery official documentation: Redis/RabbitMQ broker options, JSON serialization, worker runtime, monitoring, and reliability tradeoffs.
- Microsoft identity platform: OpenID Connect for web apps and tenant-scoped sign-in.
- Microsoft Graph: `Mail.Send` permissions for notification mail.
- Power BI Embedded: service principal, workspace access, capacity and admin settings.
- Human-centered design references: Digital.gov HCD approach, ISO 9241-210, accessibility guidance.
- MEL/MEAL references: OECD DAC evaluation criteria, IFRC monitoring and evaluation guidance, BetterEvaluation.
- ODK ecosystem references: ODK Central introduction/API/form management, ODK XLSForm reference, ODK XForms specification, XLSForm.org, `pyxform`, and KoboToolbox web-form/draft behavior.
- Current Power Pages form-runner references:
  - `/home/jmduda/KodeX/crdb-mel/scripts/xlsform-compile.py`
  - `/home/jmduda/KodeX/crdb-mel/powerpages/webforms-spa/src/offline/xform-cache.ts`
  - `/home/jmduda/KodeX/crdb-mel/powerpages/webforms-spa/src/powerpages-api/client.ts`
  - `/home/jmduda/KodeX/crdb-mel/docs/powerpages-odk-webforms/collect-runtime-cache-delivery-20260729.md`
  - `/home/jmduda/KodeX/crdb-mel/docs/powerpages-odk-webforms/user-stories.md`

## Lessons to compound from the current prototype

1. Do not hard-code TACATDP as the platform schema. TACATDP should become the first configured programme/scheme.
2. Keep field data collection as a runtime capability, not one bespoke form screen per programme.
3. Keep baseline/import data lineage. Imported data must trace back to source file, row, form version, importer, and projection status.
4. Avoid browser-side permission fragility for privileged writes. Server-side application code should own privileged import, projection, workflow, and reporting jobs under audited roles.
5. Keep a demonstration path for CRDB Power Pages if needed, but do not let Power Pages table-permission blockers determine the final architecture.
6. Portal/dashboard lessons still apply: a dedicated visualization route, clear KPI metadata, prototype/demo data labels, and dashboard cards that distinguish financial, output, outcome, climate estimate, and operational quality metrics.
7. Preserve the ODK/XLSForm runtime boundary. Form authoring should use XLSForm-compatible workbooks or a UI that can emit the same semantics; runtime rendering should use compiled XForm-compatible artifacts rather than losing skip logic, constraints, calculations, repeats, media, and entity semantics.

## Reference architecture direction

Use a Django monolith with modular apps, not microservices for the first product.

Core runtime:

- Django web application
- PostgreSQL primary database
- Redis cache/broker
- Celery workers for long-running/background work
- Viewflow for workflow/process orchestration and Viewflow/MDC frontend foundations
- Server-rendered templates for primary shell, forms, worklists, workflow tasks, and admin/configuration screens
- Rich JavaScript islands only where justified, for example map dashboards, charting, or complex form preview

Recommended first app boundaries:

- `apps.accounts`: CRDB/Entra-backed identity bridge, local user profile, roles
- `apps.shell`: authenticated shell, navigation, topbar, footer, help, notifications entry point
- `apps.organizations`: CRDB units, departments, branches, partners, implementers
- `apps.programmes`: programmes, schemes, products, operations, components
- `apps.results`: results frameworks, outcomes, outputs, activities, logframes
- `apps.indicators`: indicator registry, targets, computation rules, data-source mappings
- `apps.forms`: form definitions, versions, XForm/web-form runtime metadata
- `apps.collection`: submissions, submission versions, attachments, evidence
- `apps.beneficiaries`: party/person/group/organization beneficiary registry
- `apps.interventions`: configurable intervention catalogue
- `apps.locations`: country/region/district/ward/village/facility/farm geometry
- `apps.workflows`: Viewflow process definitions and reusable workflow adapters
- `apps.verification`: data quality checks, review queues, approval states
- `apps.projections`: reporting fact/projection jobs, indicator result generation
- `apps.dashboards`: management dashboards and operational dashboards
- `apps.reports`: report templates, exports, scheduled report jobs
- `apps.learning`: findings, recommendations, management responses, action tracking
- `apps.integrations`: Microsoft Graph, Power BI, bank-system import/export adapters

## Form runtime and ODK ecosystem architecture

Enterprise MEAL should treat field data collection as a first-class subsystem, not as ordinary Django model forms.

The current Power Pages prototype already proved a useful architecture:

1. A source XLSForm workbook is compiled to ODK XForm XML.
2. The form definition is stored as a versioned form artifact.
3. The runtime loads XForm XML only when a user opens Collect/Edit.
4. The browser caches XForm XML in IndexedDB using a cache key based on form-version id, version, and marker/XML hash.
5. A submission writes a stable parent submission row, a new immutable submission-version row, the canonical XForm instance XML, attachments, and later reporting projections.
6. Baseline import appends or replaces through versioned rows instead of silently overwriting evidence.

The new Django architecture should keep these concepts but move privileged and fragile work server-side:

- Use `pyxform` to compile XLSForm `.xlsx` files into ODK XForm XML.
- Store both the original XLSForm file and the compiled XForm XML.
- Store form versions immutably after publication.
- Keep draft/test/publish lifecycle similar to ODK Central:
  - draft upload
  - validation
  - preview/test submissions
  - publish
  - version update with structural-change review
- Keep submission versions immutable for audit and correction history.
- Normalize reporting/projection tables asynchronously using Celery.
- Keep raw XForm instance XML as legal/source evidence even when normalized projection rows exist.
- Keep attachments/evidence linked to submission versions.

ODK Central concepts to borrow:

- Project as a sandbox for users, forms, submissions, and app users.
- Form drafts, published forms, form version updates, multimedia/form attachments, submission attachments, review/comment/edit state, OData-friendly output, and Entities/Datasets for longitudinal records.
- Public APIs as a product capability, not an afterthought.
- Entity lists for beneficiary/farm/business follow-up workflows where a later form needs to reference or update a long-lived record.

KoboToolbox concepts to borrow:

- Browser web forms support save-draft behavior.
- Drafts are local until finalized/submitted.
- Multiple-language forms and paged forms are common expectations.
- Field-user experience must survive interrupted connectivity and partial completion.

ODK ecosystem standards to preserve:

- XLSForm `survey`, `choices`, and `settings` sheets.
- XForm model/body structure.
- XPath expressions for relevance, constraints, calculations, and repeat logic.
- OpenRosa-style form/submission compatibility where useful.
- OData-like export/analytics feeds where useful, especially for Power BI.

Recommended Enterprise MEAL form subsystem apps/models:

- `FormProject` or association from `PortfolioItem` to forms.
- `FormDefinition`: stable logical form identity.
- `FormVersion`: immutable compiled version with source workbook, XForm XML, version, hash, status.
- `FormDraft`: editable upload/preview candidate.
- `FormAttachment`: media files, itemsets, external choices, form assets.
- `FormAssignment`: user/team/role assignment to form version and portfolio item.
- `Submission`: stable instance identity.
- `SubmissionVersion`: immutable submitted/corrected XML payload and metadata.
- `SubmissionAttachment`: evidence files tied to a submission version.
- `SubmissionReview`: verification, approval, rejection, correction request.
- `SubmissionProjectionJob`: background normalization/projection status.
- `SubmissionAnswer` / `SubmissionRepeatRow`: normalized reporting rows where analytics require row-level answers.
- `EntityDataset`: ODK Central-style entity list.
- `TrackedEntity`: person, organization, group, farm, facility, business, or operational asset.
- `EntityIdentifier`: customer id, phone, national id, bank reference, external id, and source-system keys.
- `EntityEvent`: longitudinal changes made by submissions or imports.

Implementation posture:

- Do not rebuild ODK semantics manually in Django forms for complex field surveys.
- Use Django/Viewflow for configuration, assignment, review, approval, import, and reporting workflows.
- Use an XForm-capable web runtime for collection/preview. If the current ODK Web Forms package remains suitable, wrap it as a controlled JavaScript island inside the Django shell. If not, research Enketo/ODK Web Forms alternatives before implementing.
- Keep local browser draft storage explicit and separately tested.
- Keep server-side validation and compile checks authoritative; browser validation is necessary but not sufficient.
- Treat `pyxform` warnings/errors as workflow artifacts that a form manager can review.

## Initial shell target

Learn from `../lims` first. It is closer to the target operational system than `../stemgen-platform`.

Adopt:

- Viewflow `Site` / `Application` registration from `apps/shell/site.py`.
- Menu grouping through `menu_group`, with primary, configuration, and hidden destinations.
- Custom `templates/viewflow/base_page.html` extending Viewflow base page.
- Custom drawer menu template preserving Viewflow/MDC anatomy.
- Tokenized CSS split:
  - `static/sfu_mel/ui/tokens.css`
  - `static/sfu_mel/ui/components.css`
  - `static/sfu_mel/ui/authenticated.css`
  - `static/sfu_mel/shell/site.css`
- Topbar pattern:
  - drawer toggle
  - active programme/context chips
  - route/title context
  - optional search
  - notification icon
  - account chip/menu
- Footer pattern:
  - environment/status
  - last sync/job status
  - copyright or internal classification

Adapt for Material 3:

- Use Material 3 design tokens for color roles, elevation, shape, spacing, typography, focus, and state layers.
- Preserve Viewflow/MDC anatomy because Viewflow frontend currently depends on MDC-style components.
- Avoid page-local styling for cards, buttons, tabs, tables, chips, and forms.
- Implement an accessible responsive shell:
  - expanded drawer on desktop
  - rail/collapsed drawer at medium widths
  - temporary drawer on mobile
  - keyboard focus states
  - semantic headings and landmarks

## Viewflow workflow automation posture

Use the LIMS dynamic-operation-runner lesson directly:

- Viewflow owns process/task lifecycle, assignment, permission checks, locking, inbox/worklist, and process history.
- The MEL platform owns programme semantics, form definitions, validation, indicator mapping, projection, evidence, and learning actions.
- Do not generate arbitrary Python `Flow` classes from database configuration at request time.
- For configurable programme workflows, compile configuration into durable execution manifests interpreted by stable Viewflow adapters.
- Use Celery for long-running tasks such as baseline import, indicator recomputation, report generation, Power BI refresh triggers, and scheduled reminders.

Candidate workflows:

- Baseline import review and approval
- Field submission verification
- Indicator result computation and approval
- Evidence review
- Report generation and sign-off
- Learning action assignment and follow-up
- Access request/onboarding
- Data correction with audit trail

## Human-centered design focus

Research and design must start from SFU’s actual working environment:

- MEL Manager
- MEL Officer
- SFU management
- branch/regional users
- field/data collectors
- data quality reviewers
- programme managers
- executives/report consumers
- external/donor/government viewers where approved

Initial HCD questions:

- What does each role need to decide weekly/monthly/quarterly?
- What evidence do they currently trust?
- Where do delays happen: collection, review, approval, reporting, or decision-making?
- What must work when internet access is poor or field users are remote?
- What reports must be defensible to CRDB, GCF, Government, auditors, and management?
- What should be self-service configuration versus developer-controlled?
- Which operations beyond programmes/schemes need MEL-style monitoring but should not be forced into a programme-only model?

Design principles:

- Use plain operational language.
- Separate management reporting, operational queues, configuration, and technical administration.
- Show data status and verification level whenever a KPI appears.
- Prefer guided setup and progressive disclosure for configuration.
- Build accessible pages from the start: keyboard navigation, visible focus, labels, helper/error text, color-independent status, and tested responsive layouts.

## MEAL/MEL capability model

The product should support Monitoring, Evaluation, Accountability, and Learning.

Monitoring:

- routine data collection
- reporting periods
- activity/output tracking
- due/overdue submissions
- verification status
- operational dashboards

Evaluation:

- baseline, midline, endline
- evaluation questions
- sampling frames
- comparison groups where applicable
- findings and evidence
- outcome/impact analysis

Accountability:

- stakeholder feedback
- complaints/grievances where approved
- consent and privacy controls
- audit trails
- reviewer decisions
- donor/government/reporting obligations

Learning:

- findings
- lessons
- recommendations
- management responses
- action owners
- deadlines
- completion status

## Configurable architecture requirements

The configurable model should support:

- programmes
- schemes
- products
- grants
- guarantee facilities
- insurance-linked products
- ESG/sustainability initiatives
- operational activities
- department workstreams

Recommended top-level concept:

`PortfolioItem`

Subtypes:

- Programme
- Scheme
- Product
- Operation
- Facility
- Initiative
- Workstream

This avoids forcing operational activities into “Programme” while still allowing shared MEL concepts:

- results framework
- indicators
- forms
- reporting periods
- locations
- organizations
- beneficiaries/parties
- interventions/activities
- workflows
- dashboards
- reports

## Microsoft integration requirements

Even with Django as the core app, CRDB Microsoft ecosystem remains important:

- Microsoft Entra ID for SSO using OIDC.
- Microsoft Graph for mailbox-backed notifications, subject to approved permissions and mailbox policy.
- Power BI/Fabric integration for future analytics, likely through service principal plus workspace permissions after admin approval.
- SharePoint/OneDrive may be document/evidence integration candidates only if CRDB approves them.
- Dataverse may remain as legacy/prototype import source or integration target, not necessarily the primary database.

Do not design around Azure CLI developer access. Use approved tenant/application registrations and deployment credentials decided by CRDB.

## Repository and Karakana harness setup

Do not create the repo until the architecture research is reviewed.

When approved:

1. Create a new repository named `ent-meal` for the Enterprise MEAL platform.
2. Add `AGENTS.md` immediately with project-specific rules.
3. Add `KARAKANA.md` immediately.
4. Register the project under Karakana:
   - `ubongo/projects/ent-meal/overview.md`
   - `architecture.md`
   - `decisions.md`
   - `known-issues.md`
   - `open-issues.md`
   - `deployment.md`
5. Add a skillpack:
   - Django/Viewflow
   - Material 3 UI
   - HCD research
   - MEL/MEAL domain modeling
   - Microsoft integration
6. Add initial ADRs:
   - Django/Viewflow platform foundation
   - PostgreSQL/Redis/Celery runtime
   - Microsoft Entra identity integration
   - Configurable programme/operation domain model
   - Viewflow workflow adapter strategy
   - Material 3/Viewflow frontend boundary
7. Add local Docker Compose for Postgres and Redis.
8. Add CI-ready checks:
   - `ruff` or equivalent linting
   - `pytest`
   - Django system checks
   - migration check
   - template/static smoke test
   - accessibility/design token guard when shell exists

## First planned vertical slice

Recommended first slice for the new repo:

1. Repo/harness bootstrap.
2. Django project with env-based settings.
3. Docker Compose: Postgres + Redis.
4. Custom user model and local admin bootstrap.
5. Viewflow installed and base shell route registered.
6. Authenticated shell:
   - side navigation
   - topbar
   - content region
   - footer
   - account menu
7. Placeholder apps registered:
   - Home
   - Worklist
   - Programmes
   - Indicators
   - Forms
   - Data Collection
   - Verification
   - Dashboards
   - Reports
   - Learning
   - Setup
8. Initial form-runtime foundation:
   - `pyxform` dependency decision;
   - XLSForm upload/compile service stub;
   - immutable `FormDefinition`/`FormVersion` model plan;
   - source XLSForm and compiled XForm artifact storage plan.
9. One smoke-tested login path:
   - local dev auth first
   - Entra/OIDC plan documented, not forced before CRDB app registration exists

Acceptance for first slice:

- `docker compose up` starts Postgres/Redis.
- `python manage.py migrate` passes.
- `python manage.py check` passes.
- `pytest` passes.
- Authenticated user can see the shell.
- Navigation is grouped and role-aware.
- Shell follows Material 3 token/spacing principles while preserving Viewflow/MDC compatibility.
- No CRDB secrets or tenant credentials are committed.

## Open questions before repo creation

- Confirm `ent-meal` as the final repository name in GitHub before creation.
- Is this a CRDB-owned repo or current workspace repo first?
- Will CRDB provide container runtime only, or also managed PostgreSQL/Redis?
- Will the first environment be internal dev only or accessible for SFU review?
- Which identity mode is approved for development: local Django users first, Entra OIDC immediately, or both?
- Is Power BI/Fabric available in the development environment, or should dashboards start inside Django?
- What is the expected migration path for already imported baseline data from the Power Pages prototype?
- Which operational activities should be modeled in the first configurable domain example alongside TACATDP?

## Recommended next action

Review this artifact, then decide whether to:

1. write the new repository/harness bootstrap task;
2. expand the domain model first; or
3. produce a CRDB infrastructure checklist for the Docker-capable Django platform.
