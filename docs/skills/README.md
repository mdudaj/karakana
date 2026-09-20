# Skill Task Protocol

## Adaptive UI review routing

Use `design-system-governance` for shared containment, component-width layouts,
scope visibility and icon/text anatomy. Its adaptive-component reference records
the diagnosis and design contract. Use `design-qa-playwright` for control-level
reflow and keyboard regressions: page scroll width alone is not an acceptance
gate. Pair with `accessibility-wcag-audit` for semantics and `viewflow-framework`
in Viewflow applications. These extend existing catalogue entries, not a parallel
design system. Project-specific fixes and evidence stay in the project.

See [adaptive UX verification delivery](adaptive-ux-verification.md) for scope,
verification and remaining catalogue follow-ups.

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
