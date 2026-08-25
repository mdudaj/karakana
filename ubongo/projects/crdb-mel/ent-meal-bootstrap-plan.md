# Enterprise MEAL Repository Bootstrap Plan

Date: 2026-08-24

Status: review-ready bootstrap plan. This plan does not create the repository yet.

Platform name: `Enterprise MEAL`

Repository name: `ent-meal`

## Purpose

Create a new Django/Viewflow platform repository for CRDB Sustainable Finance Unit's configurable Monitoring, Evaluation, Accountability, and Learning system.

The new repository should compound lessons from:

- the current Power Pages MEL prototype;
- `../lims` authenticated Viewflow shell and workflow patterns;
- `../stemgen-platform` Django/Postgres/Redis/Celery bootstrap patterns;
- ODK/XLSForm/pyxform/ODK Central/KoboToolbox form-runtime architecture;
- Microsoft-first CRDB integration requirements.

## Non-goals for bootstrap

- Do not migrate CRDB data in the bootstrap slice.
- Do not integrate live CRDB Entra ID before app registration details exist.
- Do not integrate Power BI before workspace/service-principal permissions exist.
- Do not rebuild the full MEAL domain model in slice 1.
- Do not retire or delete the current Power Pages prototype.
- Do not commit secrets, tenant credentials, `.env`, or CRDB connection strings.

## Repository location

Expected local path:

```text
/home/jmduda/KodeX/ent-meal
```

Expected remote repository name:

```text
ent-meal
```

Open decision:

- Confirm whether the first remote is under the current GitHub account/workspace or CRDB-owned GitHub/DevOps.

## Initial repository contract

Create the following files first:

```text
AGENTS.md
KARAKANA.md
README.md
.gitignore
.env.example
pyproject.toml
docker-compose.yml
manage.py
config/
apps/
docs/adr/
docs/architecture/
```

### `AGENTS.md` minimum content

The repository-specific agent instructions must state:

- Use Karakana handoff at task start/end.
- Work from evidence: project artifacts, local source, official docs, tests.
- Never commit secrets or generated runtime artifacts.
- Use task branches and reviewable commits.
- Run relevant tests before handoff.
- Do not change authentication, deployment, production data, or CRDB permissions without explicit approval.
- Keep UX work aligned with Material 3, Viewflow frontend anatomy, and human-centered design.
- Treat field forms as an XForm/XLSForm runtime subsystem, not normal Django model forms.

### `KARAKANA.md` minimum content

The project contract must define:

- project name: Enterprise MEAL;
- project id: `ent-meal`;
- stack: Django, PostgreSQL, Redis, Celery, Viewflow;
- standard commands;
- durable memory paths;
- test/verification commands;
- safety and approval rules;
- required research/ADR rules before authentication, workflow, schema, or deployment work.

## Karakana registration

Add project memory under Karakana:

```text
ubongo/projects/ent-meal/overview.md
ubongo/projects/ent-meal/architecture.md
ubongo/projects/ent-meal/decisions.md
ubongo/projects/ent-meal/known-issues.md
ubongo/projects/ent-meal/open-issues.md
ubongo/projects/ent-meal/deployment.md
```

Add skillpack:

```text
skillpacks/ent-meal.yml
```

Initial skillpack posture:

- required:
  - Django/Viewflow workflow discipline;
  - Material 3 UI governance;
  - human-centered design;
  - MEAL domain modeling;
  - XLSForm/XForm runtime;
  - Microsoft integration boundary;
  - delivery artifact gate;
  - Karakana handoff.
- protocols:
  - requirements for requirements/domain artifacts;
  - ux-change for shell and frontend behavior;
  - python-code-change for Django implementation;
  - assessment-review for research-only work;
  - skill-update when durable skills are changed.

The new project should also be added to workspace visibility if Karakana workspace commands need to list it alongside `crdb-mel`, `lims`, and `stemgen-platform`.

## Initial ADRs

Create these ADRs before or during slice 1:

```text
docs/adr/0001-django-viewflow-platform.md
docs/adr/0002-postgres-redis-celery.md
docs/adr/0003-enterprise-meal-configurable-domain.md
docs/adr/0004-xlsform-xform-runtime-subsystem.md
docs/adr/0005-microsoft-entra-integration-boundary.md
docs/adr/0006-material3-viewflow-frontend-boundary.md
docs/adr/0007-viewflow-workflow-adapter-strategy.md
```

### ADR intent

`0001`: Django and Viewflow are the application and workflow/frontend foundation.

`0002`: PostgreSQL is the application DB; Redis and Celery are required for background jobs.

`0003`: TACATDP is the first configuration; the model supports programmes, schemes, products, operations, and workstreams.

`0004`: XLSForm/XForm semantics are preserved through pyxform and an XForm-capable runtime.

`0005`: CRDB Microsoft ecosystem integration uses approved Entra/OIDC, Microsoft Graph, and Power BI service-principal patterns; do not assume Azure CLI developer access.

`0006`: UI uses Material 3 tokens while preserving Viewflow/MDC anatomy and accessibility.

`0007`: Viewflow owns process/task lifecycle; configured MEAL workflows are interpreted by stable adapters, not generated Python classes at request time.

## First vertical slice

Slice name:

```text
slice-1-shell-auth-bootstrap
```

Goal:

Deliver a runnable Django application with local authentication, a Viewflow-backed shell, placeholder navigation, Postgres/Redis configuration, and a documented XForm runtime seam.

### Implementation steps

1. Create repository and baseline files.
2. Configure Python project with:
   - Django;
   - django-viewflow;
   - psycopg;
   - redis client;
   - celery;
   - pytest;
   - ruff or equivalent linting;
   - pyxform decision recorded, optionally added if compile stub is included.
3. Add Docker Compose:
   - PostgreSQL;
   - Redis.
4. Add Django config:
   - env-file loader;
   - `DATABASE_URL` parsing;
   - `REDIS_URL`;
   - `CELERY_BROKER_URL`;
   - `CELERY_RESULT_BACKEND`;
   - `Africa/Dar_es_Salaam` timezone;
   - static/media settings;
   - safe dev defaults only.
5. Add custom user model in `apps.accounts` or `apps.users`.
6. Add local login/logout/profile path.
7. Install/register Viewflow.
8. Add `apps.shell`:
   - Viewflow `Site`;
   - `Application` classes;
   - grouped navigation metadata;
   - custom Viewflow base page;
   - custom side menu;
   - topbar;
   - footer.
9. Add placeholder apps/routes:
   - Home;
   - Worklist;
   - Programmes;
   - Indicators;
   - Forms;
   - Data Collection;
   - Verification;
   - Dashboards;
   - Reports;
   - Learning;
   - Setup.
10. Add Material 3/Viewflow token CSS:
    - `static/ent_meal/ui/tokens.css`;
    - `static/ent_meal/ui/components.css`;
    - `static/ent_meal/ui/authenticated.css`;
    - `static/ent_meal/shell/site.css`.
11. Add minimal form-runtime seam:
    - app placeholder `apps.forms`;
    - model sketch or ADR for `FormDefinition`, `FormVersion`, `FormDraft`;
    - service stub/interface for XLSForm compile;
    - no production upload path yet.
12. Add tests:
    - settings import;
    - URL resolution;
    - authenticated shell renders;
    - navigation grouping;
    - Django system check;
    - no committed `.env`.

## Initial information architecture

Use a compact shell derived from `../lims`, adapted for Enterprise MEAL.

Primary navigation:

- Home
- Worklist
- Programmes
- Data Collection
- Verification
- Dashboards
- Reports
- Learning

Configuration / Setup:

- Organizations
- Indicators
- Forms
- Results Frameworks
- Portfolio Items
- Users and Roles

Hidden/account routes:

- Profile
- Change password
- Notifications
- Help

The shell should support an active context area for:

- active portfolio item/programme;
- reporting period;
- environment;
- role or unit.

## Form runtime seam for slice 1

Do not build a full form runner in slice 1.

Deliver only:

- architecture ADR;
- model/interface names;
- compile service contract;
- storage path decision;
- test fixture placeholder.

Minimum service contract:

```python
class XlsFormCompileResult:
    form_id: str
    version: str
    title: str
    xform_xml: str
    warnings: list[str]
    itemsets: dict[str, str]


class XlsFormCompiler:
    def compile(self, workbook_file) -> XlsFormCompileResult:
        ...
```

Rules:

- pyxform warnings must be captured.
- source XLSForm must be retained.
- compiled XForm must be immutable once published.
- publish must be separate from upload/compile.
- browser collection runtime will be a later JavaScript island.

## Microsoft integration boundary for slice 1

Start with local Django auth for development.

Document but do not implement Entra/OIDC until CRDB provides:

- tenant id;
- app registration;
- redirect URI approval;
- client id;
- secret or certificate handling path;
- group/role claim strategy;
- logout URL requirements.

Document but do not implement Microsoft Graph mail until CRDB provides:

- sender mailbox;
- Graph permission approval;
- delegated vs application permission decision;
- mailbox application access policy if application permission is used.

Document but do not implement Power BI until CRDB provides:

- workspace;
- service principal/app user approval;
- Fabric/Power BI admin setting;
- capacity/licensing decision;
- embed mode decision.

## Verification gates

Local commands expected after slice 1:

```bash
docker compose up -d postgres redis
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python manage.py check
.venv/bin/python manage.py migrate
.venv/bin/pytest
```

Karakana commands:

```bash
karakana handoff load --project ent-meal --skillpack ent-meal
karakana memory validate --project ent-meal
karakana skillpack validate ent-meal
karakana handoff refresh --project ent-meal --skillpack ent-meal --purpose "End of task handoff"
```

Acceptance criteria:

- App starts locally.
- Postgres and Redis run through Docker Compose.
- Django checks and migrations pass.
- Login/logout works with local dev user.
- Authenticated shell renders side nav, topbar, content region, and footer.
- Placeholder routes resolve.
- Shell uses shared tokens/components, not page-local styling.
- No secrets are committed.
- ADRs explain all foundation decisions.
- Karakana can load and validate the new project memory.

## Risks and controls

| Risk | Control |
|---|---|
| Bootstrap becomes architecture-heavy and delays visible UI | Slice 1 ends at shell/auth/placeholders plus documented seams. |
| Viewflow frontend assumptions drift from Material 3 | Preserve Viewflow/MDC anatomy and implement Material 3 through tokens and components. |
| Form runtime becomes a custom Django form builder | Preserve XLSForm/XForm semantics and defer runner implementation to a separate researched slice. |
| Microsoft auth blocks local progress | Use local auth first; document Entra/OIDC boundary. |
| CRDB Docker environment details are incomplete | Use local Docker Compose first; keep deployment docs as assumptions until CRDB confirms. |
| Power Pages prototype lessons are lost | Link `crdb-mel` research and keep migration/integration as a later slice. |

## Open decisions before implementation

1. Confirm remote ownership for `ent-meal`.
2. Confirm whether to create the repo locally first or remote first.
3. Confirm whether `pyxform` is installed in slice 1 or only documented with an interface.
4. Confirm initial auth mode: local-only first, or local plus Entra config placeholders.
5. Confirm whether project memory for `ent-meal` should live in Karakana before or during repo creation.
6. Confirm first UI branding: `Enterprise MEAL`, `CRDB Sustainable Finance Unit`, or both.

## Recommended next action

After review approval:

1. Create `../ent-meal`.
2. Add repository contract files.
3. Add Karakana project memory and skillpack.
4. Implement slice 1 shell/auth bootstrap.
5. Validate and commit.
