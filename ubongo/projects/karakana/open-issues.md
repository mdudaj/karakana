# Karakana Open Issues

This is the repository-owned development backlog for Karakana. Each active item
has one stable ID, priority, evidence, acceptance and next action. A GitHub issue
may link to an item, but this file remains the reviewed source for its project
scope and state. Use `- [ ]` for active items and `- [x]` only after verification;
handoffs link this file when it contains active items. Audience research and
project-specific pilot tasks belong in their own records, not here.

Priorities: **P1** changes a control-plane decision or safety-relevant result;
**P2** makes planned work reliable and discoverable; **P3** is maintenance with
no current blocker. Priority is a triage judgment, not an approval or release
claim. Review this file against current source and runtime evidence at each task.

## Active development items

- [ ] **KDX-04 · P3 · proposed — reconcile catalogue status wording.**
  Evidence: `docs/skills/engineering-artifact-catalogue/PLAN.md` still calls
  P06 integration pending, although the catalogue merged in PR #13 and the
  executive pilot records merged in PRs #18–20. Acceptance: update the canonical
  Markdown state without changing the frozen XLSX/JSON or pretending that real
  reader acceptance has occurred. Next: make a bounded documentation patch
  after current P1/P2 delivery.
- [ ] **KDX-06 · P2 · proposed — require project-specific requirements content.**
  Evidence: requirement `20261001-154449-req-565169` reports ready, but its
  generated PRD has generic user stories and functional requirements about the
  requirements generator, rather than this task's planner and backlog behavior.
  Acceptance: readiness rejects or flags a generated artifact whose goals,
  stories and criteria omit the source task's specific behavior; deterministic
  examples cover a concrete source and a generic output. Next: inspect the
  requirements generator and readiness rules before a bounded change.
- [ ] **KDX-07 · P3 · proposed — reconcile optional project paths.**
  Evidence: dogfood `20261001-160648-dogfood-b3997b` warns that `billing`,
  `msc-research`, and `nhrdm` skillpacks point at absent memory directories;
  workspace validation also finds absent sibling paths for `nhrdm`, `nhrils`,
  and `billing`. Acceptance: each memory and workspace path is restored,
  corrected or explicitly retired after checking project ownership; validation
  no longer emits stale-path warnings. Next: review those skillpacks and
  workspace definitions with their project owners before changing configuration.

## Completed development items

These items passed local verification. PR #21 records integration of KDX-01–03;
KDX-05 integration is tracked in its own PR. Checklist completion does not imply
deployment or user acceptance.

- [x] **KDX-01 · P1 · merged — reject incidental note priority tokens.**
  Evidence: run `20261001-153048-milestone-0036ff` misread historical `P06`
  as P0. An explicit-line parser and positive/negative regression tests now
  preserve `P0:`/`P1:` blockers and structured dogfood priorities. CLI check
  `20261001-154711-milestone-b40f27` reports no blocker for historical/negated
  prose. Integrated via PR #21. Next: continue KDX-06.
- [x] **KDX-02 · P2 · merged — expose the development backlog.**
  Evidence: the former file was an empty template; it now has stable IDs and
  task state. Isolated tests show that handoffs link only their own active
  project backlog, including with artifact recovery disabled. Memory validation
  passed. Integrated via PR #21. Next: continue KDX-06.
- [x] **KDX-03 · P2 · merged — refresh dogfood and requirements.**
  Evidence: dogfood `20261001-154355-dogfood-c4944f` ran the safe full
  allowlist; the five warnings were triaged in the delivery record. Requirements
  `20261001-154449-req-565169` were inspected: structural readiness passed,
  but the generated PRD is generic and is not accepted as task authority. The
  project-specific requirements remain in the reviewed delivery record.
  Integrated via PR #21. Next: take KDX-06.
- [x] **KDX-05 · P2 · locally verified — classify dogfood warnings accurately.**
  Evidence: run `20261001-154355-dogfood-c4944f` misclassified `warnings: 0`
  and a warning section heading. The focused regressions and full dogfood run
  `20261001-160648-dogfood-b3997b` show zero-count eval, optional doctor
  credentials, and workspace `- None` as passed; real skillpack/workspace
  warnings retain their messages. Next: verify integration through its PR,
  then take KDX-06.
