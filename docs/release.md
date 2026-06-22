# Karakana Release Process

Release commands are local and draft-only.

## Check Readiness

```bash
karakana release check
karakana release check --full
```

The default check is lightweight. `--full` runs validation, evals, and tests.

## Draft Notes

```bash
karakana release notes --version 0.1.0
```

Release notes are generated from local evidence and must be reviewed before use.

## Checklist

```bash
karakana release checklist
```

## Manual Release

Tagging, package publishing, GitHub releases, pushing, and deployment are manual steps outside Karakana automation for this milestone.
