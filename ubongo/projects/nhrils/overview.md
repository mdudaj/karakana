# NHRILS Overview

NHRILS is the NIMR integrated library system project based on `inveniosoftware/invenio-app-ils`.

The repository is newly introduced into the NIMR workspace. Until user-provided library/system documents are reviewed, treat the codebase as an upstream Invenio-App-ILS baseline plus any existing NIMR fork changes.

## Current Intent

- Establish clean Git remotes before customization:
  - `upstream`: `git@github.com:inveniosoftware/invenio-app-ils.git`
  - `origin`: `git@github.com:nimr-tz/nhrils.git`
- Load project docs before requirements, architecture, data model, circulation, patron, acquisition, OPAC, or UI customization.
- Configure project-specific skills only after documents clarify NIMR library workflows, users, integrations, cataloging standards, and deployment constraints.

## Required Skill

Use `invenio-framework` for general Invenio service/resource/schema/config/permission/index work.
Use `invenio-ils-customization` before NHRILS catalogue, circulation, patron, item/e-item, search/facet, backoffice, statistics, notification, or ILS UI/theme work.

## Safety

- Do not change authentication, permissions, migrations, OpenSearch mappings, or production configuration without explicit approval.
- Do not push or overwrite the NIMR remote until the local branch relationship to `origin/master` and `upstream/master` is verified.
- Do not import real patron, circulation, acquisition, or bibliographic data into a development environment without privacy and data-ownership review.

## First Files To Inspect

- `docs/NHRILS_INITIAL_CUSTOMIZATION_AND_ROLLOUT_PLAN.md`
- `docs/NHRILS_CATALOGUE_MVP_20260804.md`
- `docs/NHRILS_UX_DESIGN_SYSTEM_20260804.md`
- `README.md`
- `pyproject.toml`
- `docker-compose.yml`
- `README.rst`
- `invenio_app_ils/config.py`
- `invenio_app_ils/ext.py`
- `invenio_app_ils/permissions.py`
- `invenio_app_ils/search_permissions.py`
- `invenio_app_ils/documents/`
- `invenio_app_ils/series/`
- `invenio_app_ils/literature/`
- `invenio_app_ils/items/`
- `invenio_app_ils/eitems/`
- `invenio_app_ils/patrons/`
- `invenio_app_ils/circulation/`
- `invenio_app_ils/vocabularies/`
- `invenio_app_ils/assets/`
- `invenio_app_ils/static/css/`
- `invenio_app_ils/templates/`
- `tests/`

## Pending Context

The user will provide documentation to guide NHRILS requirements, customization boundaries, and any project-specific skill additions.
