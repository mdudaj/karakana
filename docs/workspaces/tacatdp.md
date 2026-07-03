# TACATDP Workspace Notes

TACATDP is registered as a managed project for Power Apps canvas app and Microsoft Lists delivery.

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
- Primary skill: `skills/power-platform-canvas-apps/SKILL.md`
- OKF project concept: `okf/projects/tacatdp/project.md`
- OKF skillpack concept: `okf/projects/tacatdp/skillpack.md`
