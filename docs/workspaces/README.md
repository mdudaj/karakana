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

## End Every Task

```bash
karakana handoff refresh --workspace <workspace> --project <project> --skillpack <skillpack> --purpose "End of task handoff"
```

Workspace status handoffs and project session handoffs remain separate artifacts.
