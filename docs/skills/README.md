# Skill Task Protocol

## Start Every Task

```bash
karakana handoff load --project <project> --skillpack <skillpack>
```

If the console script is unavailable in a fresh shell, run the same command through the project virtualenv:

```bash
.venv/bin/karakana handoff load --project <project> --skillpack <skillpack>
```

Read mandatory repository instructions, then inspect only the handoff's `Files to Inspect First`. Treat `Files Not to Reread` as advisory and verify recovered context.

## End Every Task

```bash
karakana handoff refresh --project <project> --skillpack <skillpack> --purpose "End of task handoff"
```

Run handoff doctor when references, freshness, project scope, suggested skills, or redaction are uncertain.
