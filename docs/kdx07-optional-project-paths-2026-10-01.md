# KDX-07: project memory and optional checkouts

Status: locally verified and integrated via squash merge PR #26 (`e08b50c`).
Task trace: `20261001-183225-c8d6de` (the earlier automatic memory classification
`20261001-183218-c5ad19` was superseded because this change also touches the
workspace validator).

## Classification and requirements note

KDX-07 is P3 harness configuration maintenance. The user authorized execution
of the next backlog task. GitHub publication and merge remain separate actions.
The repository contract, `docs/engineering-process.md`, the
`delivery-artifact-gate` and `karakana-self-improvement` skills govern delivery.

At task start, `skillpack validate-all` reported missing memory for `billing`,
`msc-research` and `nhrdm`. `workspace validate-all` reported missing
local paths for `nhrdm`, `nhrils` and `billing`. The three memory directories
were never committed. The NIMR workspace intentionally sets
`require_existing_paths: false`; its missing local checkouts are currently
reported as warnings. On 2026-10-01, read-only GitHub repository metadata
confirmed NIMR-owned repositories for all three registered projects; none is
checked out under this Karakana repository's sibling directory. Remote
repository names do not establish the desired local folder names, so the
existing local path aliases are retained. `docs/skillpacks.md` explicitly
retains `msc-research` for manuscript writing, separate from the
`msc-platform` implementation repository.
No manuscript repository was identified in the available project records.

Research resolution: the warnings represent absent memory and intentionally
absent local checkouts, not evidence that the registered NIMR projects should
be deleted. The selected requirement is complete, source-bound memory plus an
explicit optional checkout state. The selected method keeps ordinary missing
paths actionable and keeps checkout presence visible in status. This closes
the local configuration decision as `ready_for_implementation`; the resulting
patch is now locally verified. The requirements, schema/example, tests and
handoff dispositions are recorded below. No product-owner decision is inferred
for the missing manuscript source or any NIMR project-specific workflow.

## Product requirement and user story

An operator validating this Karakana checkout needs complete, honest project
memory and a clean signal for broken paths. A registered NIMR project may be
absent locally without becoming a stale configuration warning. As that
operator, I can see that a checkout is absent in workspace status while
validation warns about missing paths only when a local checkout is expected.

Scope: restore source-bound memory for the three registered skillpacks, mark
the three absent NIMR checkouts explicitly optional, and reconcile backlog
status.
Do not clone or modify another project, invent manuscript ownership, alter
skillpack routing/safety policy, or mark an absent checkout present.

## Acceptance criteria and definition of done

| ID | Observable result | Evidence |
| --- | --- | --- |
| AC1 | `karakana memory validate` succeeds for `billing`, `msc-research` and `nhrdm`; their memory identifies confirmed scope and unverified details. | Memory validation and manual source review. |
| AC2 | `skillpack validate-all` emits no missing-memory warning. | CLI output. |
| AC3 | `workspace validate-all` emits no warning for explicitly optional absent checkouts, while default missing paths still warn and strict required paths still error. | Isolated validator tests and CLI output. |
| AC4 | Workspace status still reports `path_exists: false` for absent optional checkouts; invalid optional-checkout values fail validation. | Isolated status and validator tests. |
| AC5 | Existing local path aliases remain explicit; KDX-04 is recorded as merged in PR #25 and KDX-07 as locally verified only after tests pass. | YAML/backlog diff and GitHub PR #25. |

Done means focused and broader relevant checks pass, the branch diff has no
blocking findings, and the append-only handoff names any unverified project
facts. A local commit is not a merge, deployment or project-owner acceptance.

## Design, traceability and artifact readiness

Add `optional_checkout: bool = false` to each workspace project. The validator
keeps the existing warning for a missing default checkout and the existing
error when workspace-wide `require_existing_paths` is true. It accepts an
absent optional checkout without a warning. Workspace status keeps its
`path_exists` value and omits only the expected missing-path warning. Explicit
boolean validation prevents a quoted string from silently changing meaning.

Use the six existing Ubongo project-memory filenames for each restored
project. State only what the skillpacks, repository metadata and project
records support. An unknown architecture, deployment target or decision is
recorded as unknown. `msc-research` must remain distinct from `msc-platform`.
The required memory files are content-bearing, not empty validator placards.

AC1–AC2 map to new `ubongo/projects/{billing,msc-research,nhrdm}/` records.
AC3–AC4 map to `karakana/workspaces/{schemas,validator,status}.py`,
`workspaces/nimr.yml`, `docs/workspaces.md` and focused tests. AC5 maps to
`workspaces/nimr.yml` and `ubongo/projects/karakana/open-issues.md`.

Rejected approaches: local cloning would only clean this machine's warnings;
removing real NIMR projects would lose workspace visibility; suppressing every
missing-path warning would hide broken required checkouts. The optional flag
is reversible. Its main risk is that a missing optional checkout becomes less
prominent in validation, so workspace status must continue to expose
`path_exists: false` and documentation must tell operators to check it before
project work.

No separate ADR, UX artifact, migration or deployment plan is required: this
is a small, reversible validation/configuration rule with a documented CLI
status effect, no visual interface and no persisted data migration. The YAML
example and regression tests are the
schema/example evidence. This document supplies the requirements note, PRD,
story, acceptance, traceability, readiness and test rationale for the task.

## Implementation instructions and verification plan

1. Inspect the named skillpacks, `workspaces/nimr.yml`, the workspace
   schema/validator/status code and existing isolated tests. Recheck project
   ownership before adding any project-specific fact.
2. Add source-bound memory; add the optional checkout field and validate its
   type; update the three NIMR entries; update workspace docs.
3. Add isolated tests for optional/default/strict/invalid states and for
   truthful status reporting. Update tests that assumed warnings from the
   developer's current checkout.
4. Run focused workspace/skillpack/memory tests, project memory validations,
   `skillpack validate-all`, `workspace validate-all`, `skill validate-all`,
   deterministic evals and the full `pytest` gate. Review the actual outcomes.
5. Update the backlog's verified state, inspect the final diff, commit on the
   task branch and refresh the handoff bound to this trace.

Rollback is a PR revert; there is no database or external repository mutation.

## Verification summary and change summary

Implemented on `fix/kdx07-optional-project-paths`:

- Added six source-bound memory files each for `billing`, `nhrdm` and
  `msc-research`; they identify unverified project details instead of inventing
  architecture, deployment or manuscript authority.
- Added `optional_checkout` to workspace project schema, validator and status;
  marked the three absent NIMR checkouts optional and documented the semantics.
  The local path aliases remain unchanged.
- Added isolated regressions for optional, default, strict and invalid values;
  kept missing-memory warnings covered. Updated the Karakana backlog with
  KDX-04 PR #25 integration and KDX-07 local state.

Verification on 2026-10-01:

| Check | Result |
| --- | --- |
| Focused workspace, skillpack and memory tests | 17 passed. |
| Full `pytest -q` | 728 passed. |
| `karakana eval run` | 173 passed, 0 failed, 0 warnings; run `20261001-183757-eval-1a0c94`. |
| `karakana skill validate-all` | Passed. |
| `karakana skillpack validate-all` and `workspace validate-all` | Passed without warnings. |
| `karakana memory validate --project` for the three restored projects | All complete. |
| `karakana workspace status --workspace nimr --json` | Status `ok`, no warnings; `nhrdm`, `nhrils` and `billing` have `path_exists: false` and `memory_exists: true`. |
| `git diff --cached --check` | Passed on the staged patch; recheck at commit. |

Residual limit: the three NIMR source repositories are absent locally, so no
project source, tests, deployment or recipient workflow was validated. The
manuscript source and owner remain unidentified. `optional_checkout` only
classifies expected local absence; it does not make a project ready for code
work. No GitHub write, merge or deployment was performed for this slice.

Integration update (2026-10-01): PR #26 was squash merged into `main`. The
post-merge safe dogfood assessment is recorded in
`docs/karakana-dogfood-assessment-2026-10-01.md`.
