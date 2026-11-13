# Portable handoff load

## Scope and authority

The owner requires a loaded handoff to carry all continuation instructions. This is a bounded correction to the previously authorised portable handoff and `main` publication. No documentation skills, Python CLI behaviour, hooks, client artifacts, deployment, credentials or model execution change.

User story: as the owner switching to Ubuntu, I load the handoff once and the agent receives the branch, current state, scope, acceptance, verification limits and next actions without another chat explanation.

## Requirements and acceptance

| ID | Requirement and acceptance | Verification |
| --- | --- | --- |
| PHL-1 | The ordinary `handoff load` output contains the complete tracked continuation note as its Next Task Brief. No `--details` or second file-reading instruction is needed to discover the task. | Refresh/load through the actual CLI and assert the full note and required sections occur in captured output. |
| PHL-2 | A single portable Bash command creates the local context from tracked text and loads it. Find CLI on PATH or in `.venv/bin`; stop clearly when neither exists. | Wrapper success and unavailable-CLI checks in temporary repositories; Bash syntax check. |
| PHL-3 | A failed refresh prevents load, errors propagate, and existing runtime history is retained. The wrapper does not install tools, switch branches, publish, call models or alter source. | Stub-CLI negative case and source review. No deletion or auto-execution commands. |
| PHL-4 | Loaded instructions include how to update `main`, switch to the continuation branch, reuse research and implement only the bounded first slice. Loading is not execution authority beyond the recorded scope. | Full-note content assertions and live local load observation. |

## Design and plan

`karakana/handoffs/summary.py::render_session_start` prints `next_task_brief` in the default load. The prior bootstrap supplied only a short pointer, while the full note went to `from_note`. Reuse the existing supported field: supply the complete tracked note to both fields, then load. No Python loader or schema change is necessary.

Add `docs/skills/engineering-artifact-catalogue/RESUME-UBUNTU.sh`. Resolve the repository relative to the wrapper, check the note and research file and available CLI, then call refresh with `--no-recover-artifacts` and the complete brief. Call load only after successful refresh. Update the tracked Ubuntu note to distinguish bootstrap from agent instructions and reflect PR #33's actual merge. Add focused wrapper checks using temporary repositories and a stub CLI; observe actual rendering separately in the real authorised handoff operation. Do not use working-checkout runtime files for tests.

The alternative is a new Python import/load API or hook change. It is unnecessary for this one portable continuation and would expand compatibility/testing scope. This wrapper uses current CLI capabilities and leaves shared routing untouched.

## Artifact readiness and definition of done

This compact record provides the classification, requirements, acceptance, design, user story, plan, test rationale and traceability for PHL-1 through PHL-4. Source evidence: `karakana/cli.py` handoff refresh/load options; `karakana/handoffs/summary.py` default output; the existing tracked Ubuntu note and proposal. No new research or architectural decision record is needed for reusing an existing field. Run the task pre-implementation gate before adding the wrapper. Completion requires focused checks, a real load observation, reviewed diff, PR check, authorised squash integration and append-only handoff. Keep implemented/verified/merged states distinct.

## Verification and continuation

Implemented: the wrapper passes the complete note as both context and visible Next Task Brief. The note states that import is complete when encountered in loaded output, so the agent proceeds rather than recursively rerunning bootstrap. The note also records PR #33's actual merge and branch state.

Verification: `bash -n docs/skills/engineering-artifact-catalogue/RESUME-UBUNTU.sh` passed. `python tests/test_portable_handoff_resume.py` passed four temporary-repository cases: PATH CLI, `.venv` fallback, failed refresh stopping load, and unavailable CLI guidance. Tests use only a stub CLI and preserve a history sentinel; no network or real runtime store is used. An authorised real refresh/load operation separately confirmed that the complete tracked note and all continuation sections appear in default load output without `--details`. `git diff --check` passed.

Full harness regression was not run because no shared Python, routing or schema code changed. This does not certify an Ubuntu installation; the wrapper checks prerequisites there. Integration follows the existing owner-authorised handoff/main correction. Next product work remains the first convention/templates slice, followed by checks/enforcement and the later Jovina review. End with a trace-bound append-only runtime handoff containing the complete note in `next_task_brief`; do not replace it with a pointer.
