# TACATDP Workspace Notes

TACATDP is registered as a managed project for Power Pages, Dataverse, and legacy Power Apps canvas app delivery context.

## Start Every TACATDP Task

```bash
karakana handoff load --workspace default --project tacatdp --skillpack tacatdp --okf-tag tacatdp --okf-limit 12
```

If the console script is unavailable:

```bash
.venv/bin/karakana handoff load --workspace default --project tacatdp --skillpack tacatdp --okf-tag tacatdp --okf-limit 12
```

## End Every TACATDP Task

```bash
karakana handoff refresh --workspace default --project tacatdp --skillpack tacatdp --purpose "End of TACATDP task handoff"
```

## Required Context

- Project memory: `ubongo/projects/tacatdp/`
- Skillpack: `skillpacks/tacatdp.yml`
- Primary field-app skill: `skills/power-pages-odk-webforms/SKILL.md`
- Admin/bootstrap skill: `skills/power-platform-cli-admin/SKILL.md`
- Legacy Canvas context skill: `skills/power-platform-canvas-apps/SKILL.md`
- OKF project concept: `okf/projects/tacatdp/project.md`
- OKF skillpack concept: `okf/projects/tacatdp/skillpack.md`

## Recurring Power Pages Access Rule

For private developer/non-production Power Pages sites, a non-admin user must be granted Site visibility access before invitation redemption can complete. This is separate from TACATDP Contact, Web Role, Table Permission, Invitation, and assignment setup.
