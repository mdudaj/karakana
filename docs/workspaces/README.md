# Workspace Task Protocol

## Start Every Task

```bash
karakana handoff load --workspace <workspace> --project <project> --skillpack <skillpack>
```

If the console script is unavailable in a fresh shell, run the same command through the project virtualenv:

```bash
.venv/bin/karakana handoff load --workspace <workspace> --project <project> --skillpack <skillpack>
```

Use only the selected project's memory, skillpack, path, and referenced artifacts.

## Registered Projects

| Project | Workspace | Memory | Skillpack | Notes |
| --- | --- | --- | --- | --- |
| `karakana` | `default` | `ubongo/projects/karakana` | `skillpacks/karakana.yml` | Harness self-improvement and safety workflows. |
| `tacatdp` | `default` | `ubongo/projects/tacatdp` | `skillpacks/tacatdp.yml` | Power Apps canvas app and Microsoft Lists delivery. |

For TACATDP-specific instructions, see `docs/workspaces/tacatdp.md`.

## End Every Task

```bash
karakana handoff refresh --workspace <workspace> --project <project> --skillpack <skillpack> --purpose "End of task handoff"
```

Workspace status handoffs and project session handoffs remain separate artifacts.
