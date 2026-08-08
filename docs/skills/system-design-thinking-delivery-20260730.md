# System Design Thinking Skill Delivery - 2026-07-30

## Task Classification

Skill update for the Karakana harness. Medium risk because the skill can affect
planning behavior for architecture, workflow, permission, UX, reporting, and
deployment decisions, but it does not execute writes or change production
systems.

## Requirements Note

Add a Karakana-native `system-design-thinking` skill that helps agents reason
about whole systems before consequential changes. The skill should be inspired
by the phase-based structure observed in `ysskrishna/ai-agent-skills`, but it
must be adapted to Karakana's artifact, approval, safety, verification, and
project-skillpack conventions.

The skill must:

- force boundary, actor, structure, dynamics, delay, leverage, design-rule,
  delivery-slice, and backfire-risk analysis;
- apply to platform UX, access control, reporting, workflow, performance,
  integration, and architecture work;
- preserve approval gates for schema, permission, authentication, production,
  deployment, and safety changes;
- avoid broad catch-all behavior by defining when not to use it;
- include eval coverage.

## Test or Eval Rationale

Two evals were added:

- `platform-ux-system-map.yml` checks that the skill maps dashboard/access UX
  as a system before slicing.
- `performance-workflow-leverage.yml` checks that the skill treats loading and
  workflow performance work as system behavior with delays, feedback,
  reversibility, non-goals, and verification.

These evals cover the two recurring pain points that motivated the skill:
page-by-page UX changes and performance/workflow changes that need broader
system reasoning.

## Trace

Protocol trace: `20260730-094225-ad0f4d`.

Implementation surfaces:

- `skills/system-design-thinking/SKILL.md`
- `skills/system-design-thinking/evals/platform-ux-system-map.yml`
- `skills/system-design-thinking/evals/performance-workflow-leverage.yml`
- `skillpacks/karakana.yml`
- `skillpacks/crdb-mel.yml`
- `skills/README.md`

## Verification Summary

Commands run:

```bash
karakana skill validate skills/system-design-thinking
karakana skill validate-all
karakana eval run --skill system-design-thinking
karakana skillpack validate-all
karakana skill index --write
```

Results:

- `karakana skill validate skills/system-design-thinking` passed.
- `karakana eval run --skill system-design-thinking` passed: 2 cases, 2
  passed, 0 failed.
- `karakana skill index --write` updated `skills/README.md`.
- `karakana skill validate-all` passed.
- `karakana skillpack validate-all` passed. Existing warnings remain for
  unrelated missing memory paths in some skillpacks: `billing`, `lims`,
  `msc-research`, and `nhrdm`.

## External Repository Lesson

The referenced `ysskrishna/ai-agent-skills` repository uses concise,
phase-based cognitive skills with clear trigger descriptions, explicit
run-order, execution rules, and a final checklist. Karakana adopted that
pattern, but the delivered skill is adapted to Karakana's own safety model:
artifact gates, approval gates, permission/schema/production cautions, evals,
skillpacks, and generated skill index.

