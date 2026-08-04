# NHRILS Architecture

NHRILS starts from Invenio-App-ILS.

Initial architecture assumptions, pending document review:

- Backend: Flask/Invenio application modules under `invenio_app_ils/`.
- Domain areas: documents, items, patrons, circulation, acquisitions, providers, interlibrary loan, vocabularies, files, notifications, and statistics.
- Search: Invenio/OpenSearch mappings and indexers.
- Data model: Invenio records plus SQLAlchemy models where provided by upstream modules.
- Frontend/admin: Invenio assets, templates, backoffice, and OPAC surfaces.

Do not finalize NIMR-specific architecture until the user-provided library documentation is reviewed.
