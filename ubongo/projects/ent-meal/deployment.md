# Enterprise MEAL Deployment

No production deployment exists yet.

## Development target

Local development should run with:

- Python 3.14 currently available on this machine.
- Django 6.0.5.
- django-viewflow 2.2.15.
- PostgreSQL 18 via Docker Compose.
- Redis 8 via Docker Compose.
- SQLite fallback for fast scaffold checks and tests.

## Verification commands

From `/home/jmduda/KodeX/ent-meal`:

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py migrate --noinput
.venv/bin/pytest -q
```

## Deployment constraints

- Do not deploy until CRDB confirms the target environment and Microsoft tenant permissions.
- Do not commit `.env`, tenant secrets, Graph credentials, database passwords, or private keys.
- Treat Microsoft Entra, Graph, and Power BI settings as environment configuration.
