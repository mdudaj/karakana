# LIMS Deployment

## Local Preview

Use the repository script:

```bash
./scripts/local_preview.sh up
./scripts/local_preview.sh dev
```

Useful commands:

```bash
./scripts/local_preview.sh check
./scripts/local_preview.sh test apps.users apps.shell apps.operations apps.runtime apps.specimens apps.storage apps.reference
./scripts/local_preview.sh browser-test
./scripts/local_preview.sh create-superuser
```

Seed published operations against the local preview database:

```bash
env DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:55433/lims .venv/bin/python manage.py seed_operations
```

As verified on 2026-08-12:

- Docker-backed `./scripts/local_preview.sh check` passed.
- `./scripts/local_preview.sh up` applied all migrations.
- `seed_operations` created `specimen-accession accession-v5`.
- `./scripts/local_preview.sh dev` started Django plus a local Celery worker.
- `http://127.0.0.1:8000/` returned `302` to `./dashboard/`.

## Production Direction

Deployment readiness is documented for the NIMR `msmt-02` Kubernetes cluster
through the `platform-gitops` Argo CD workflow.

The app runtime contract includes:

- Dockerfile
- non-root gunicorn runtime
- `/healthz` unauthenticated database readiness endpoint
- static/media collection paths
- production settings for secret key, debug, hosts, CSRF origins, database,
  Redis/Celery, SMTP, and Traefik forwarded HTTPS settings

Production deployment, production secrets, live cluster changes, and GitOps
mutation require explicit approval.

## SMTP

The app supports SMTP through Django email settings. Local `.env` and production
secret stores may set:

- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`
- `EMAIL_USE_SSL`
- `DEFAULT_FROM_EMAIL`
- `SERVER_EMAIL`

For Gmail, use `smtp.gmail.com`, port `587`, TLS enabled, and a Gmail app
password stored only in local `.env` or deployment secrets.

## Known Verification Constraint

The local preview path depends on Docker access. Direct SQLite fallback can run
`manage.py check`, but cannot run the full migration/test path because the
current migrations include PostgreSQL-specific SQL.
