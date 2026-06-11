# Karakana Troubleshooting

## Missing `.karakana`

Run `karakana doctor`; the command creates local report directories as needed.

## Missing Skills

Run:

```bash
karakana skill validate-all
```

## Invalid Skillpack or Workspace

```bash
karakana skillpack validate-all
karakana workspace validate-all
```

Starter workspaces may warn when external project paths do not exist.

## Missing pytest or git

`karakana doctor` reports these as warnings. Install them locally if you need tests or git-backed release notes.

## Codex CLI Not Found

This is a warning unless you explicitly request Codex execution.

## Provider Credentials Missing

Missing provider credentials are warnings. Dry-run tests and evals do not need them.

## Eval Failures

Open the report under `.karakana/eval-runs/<run-id>/` and inspect failed cases.

## Patch Gate Blocked

Open `.karakana/patch-gates/<gate-run-id>/gate.md` and resolve blocking safety findings before applying or committing.
