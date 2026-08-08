# Sustainable Finance MEL Platform Workspace Notes

Sustainable Finance MEL Platform is registered as a managed project for Power Pages and Dataverse delivery context. TACATDP monitoring is the first proof-of-concept use case.

## Start every Sustainable Finance MEL Platform task

```bash
karakana handoff load --workspace default --project crdb-mel --skillpack crdb-mel --okf-tag crdb-mel --okf-limit 12
```

If the console script is unavailable:

```bash
.venv/bin/karakana handoff load --workspace default --project crdb-mel --skillpack crdb-mel --okf-tag crdb-mel --okf-limit 12
```

## End every Sustainable Finance MEL Platform task

```bash
karakana handoff refresh --workspace default --project crdb-mel --skillpack crdb-mel --purpose "End of Sustainable Finance MEL Platform task handoff"
```

## Required Context

- Project memory: `ubongo/projects/crdb-mel/`
- Skillpack: `skillpacks/crdb-mel.yml`
- Primary field-app skill: `skills/power-pages-odk-webforms/SKILL.md`
- Admin/bootstrap skill: `skills/power-platform-cli-admin/SKILL.md`
- OKF project concept: `okf/projects/crdb-mel/project.md`
- OKF skillpack concept: `okf/projects/crdb-mel/skillpack.md`

## Recurring Power Pages Access Rule

For private developer/non-production Power Pages sites, a non-admin user must be granted Site visibility access before invitation redemption can complete. This is separate from TACATDP Contact, Web Role, Table Permission, Invitation, and assignment setup.
