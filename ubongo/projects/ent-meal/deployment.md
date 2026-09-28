# Sustainability Monitoring and Reporting Platform Deployment

No production deployment exists yet.

## Preview access and release verification

As of 28 September 2026, the preview runs in the `msmt-02` GitOps cluster.
Verify its public surface before connecting VPN: HTTPS `/healthz/`, `/readyz/`,
login and a known static asset;
then an invented, absent `/media/` key. Record TLS validation, status and whether
the media response comes from Django or the static sidecar. A 404 for an absent
key is route evidence only; it does not prove that a stored private file is safe.
Check HTTP-to-HTTPS redirect separately. The 28 September 2026 public check still
found an HTTP login page, so that FR-13 gate remains open.

For internal cluster inspection, the previously verified path is the approved VPN,
then the local SSH alias `nimrhqs-cluster`, then `kubectl` on remote host `msmt-02`
with remote context `default`. **An empty local `kubectl` context is expected and
does not mean cluster access is unavailable.** The local runtime record
`.karakana/deliveries/ent-meal/20260928-fr05a-session-lifecycle/ssh-verification.md`
records the working read-only route. Verify the alias, remote hostname and context
again after the user connects VPN; do not assume the older observation remains
current. Inspect only the Argo Application `argocd/msmt-02-ent-meal`, the
`ent-meal` Deployment image/ready conditions and needed migration status. Avoid
Secrets, environment dumps, private records and mutating `kubectl` commands.

The VPN previously changed DNS for the public preview hostname and led to a
filtering/block page; this was recorded in the local runtime file
`.karakana/deliveries/ent-meal/20260927-page-loading/vpn-router-continuation.md`.
Keep public and VPN-path findings separate. If the SSH alias fails after VPN,
diagnose network access with the platform operator instead of inventing a new
local kubeconfig requirement or treating it as an application outage.

To finish FR-11/FR-13a, use a newly created, harmless test-only attachment in a
synthetic application record. Prove the direct `/media/<that-file-key>` URL is
denied, the authorized app download works and an unrelated actor is denied;
remove only the synthetic record/file through its governed path. Do not probe
existing client file keys. The `ent-meal` source record
`docs/delivery/2026-09-28-fr11-fr13a-private-media-gitops.md`
and latest `ent-meal` handoff carry the current release state; recheck them before
acting. Public checks, remote read-only inspection and target file creation are
distinct authorization steps.

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
