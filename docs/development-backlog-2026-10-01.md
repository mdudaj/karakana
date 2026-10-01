# Karakana development backlog reliability: bounded delivery record

Status: implementation authorized by the user's 2026-10-01 request to execute the first P1 and P2 development backlog items. This record governs one reviewable task branch. It does not authorize live model calls, GitHub issue creation, remote publishing, deployment or protected-branch writes.

## Evidence and outcome

At task start, the [project backlog](../ubongo/projects/karakana/open-issues.md) was an empty template. GitHub had no open issues or pull requests when checked on 2026-10-01. The latest Karakana dogfood backlog, `20260825-082113-dogfood-50388a`, had zero findings but predated the current work. `milestone next` run `20261001-153048-milestone-0036ff` interpreted historical label `P06` in a free-text note as a `P0` blocker; a control run without that label, `20261001-153202-milestone-08bdc9`, did not. The cause was the substring check in `karakana/milestones/decision.py`. Existing structured dogfood P0/P1 handling is distinct and must remain active. Recent handoffs listed the pilot backlog only inside prose and did not reference the project issue file.

The outcome is a trustworthy milestone blocker decision and a project-scoped, reviewable development backlog that future Karakana handoffs can locate. Runtime dogfood and requirements evidence will be refreshed and reviewed, not treated as product acceptance.

## Requirements and user stories

**DB-1, planning operator:** As an operator choosing Karakana's next milestone, I need historical IDs and negated mentions in notes to stay contextual, so the CLI does not invent release blockers. A note reports a priority blocker only on an explicit line of the form `P0: description` or `P1: description`; prose such as `P06`, `no P0/P1 blockers` or `P1 was closed` is not a blocker. Structured dogfood backlog priorities remain authoritative.

**DB-2, next-session agent:** As an agent loading a project handoff, I need the current project development backlog linked from the handoff when it has active items, so I can distinguish it from pilot or research follow-ups. `ubongo/projects/<project>/open-issues.md` is the single repository-owned list for open development work; GitHub issue links can be attached to items later without copying their state. Other projects' files must not appear.

**DB-3, maintainer:** As a maintainer, I need fresh project dogfood and requirements evidence after this change, so the next development slice is chosen from current findings and stated requirements rather than an August readiness label. The command receipts must name actual results and limitations. These runtime artifacts do not create GitHub issues or prove readiness by themselves.

## Acceptance criteria and traceability

| ID | Observable criterion | Governing surface | Verification |
| --- | --- | --- | --- |
| A1 / DB-1 | `P06`, `no P0/P1 blockers`, and closed/quoted mentions do not create note findings or a cleanup recommendation; an explicit `P1: unresolved ...` line does. | `karakana/milestones/decision.py`; next-milestone guidance | Focused positive/negative tests with temporary repositories. |
| A2 / DB-1 | A real structured P1 dogfood backlog still blocks strict mode and appears in findings. | Existing dogfood collector | Existing strict-mode test plus focused suite. |
| A3 / DB-2 | A nonempty project `open-issues.md` is referenced and inspected first by its own handoff, including with automatic recovery disabled; empty templates and another project's backlog are not presented as active. | `karakana/handoffs/builder.py`; project memory | Isolated handoff tests and handoff doctor. |
| A4 / DB-2 | The Karakana memory file has stable IDs, priorities, state, evidence and next action for open development items; pilot audience work stays separate. | `ubongo/projects/karakana/open-issues.md` | Manual review, memory validation and Markdown link check. |
| A5 / DB-3 | A new Karakana dogfood run and project-specific requirements are inspected; generated output is accepted only if it preserves the concrete task behavior, and limitations are disclosed. | `.karakana/dogfood/`, `.karakana/requirements/`, this record | Command receipts and semantic readiness review. |
| A6 / all | Focused tests, full required pytest/evals, skill/memory validation, protocol completion and diff review are recorded before delivery. | This record and task trace | Actual command outcomes, not artifact presence alone. |

## Design, scope and artifact choices

Choose an anchored, explicit priority line grammar rather than attempting to infer negation or priority from arbitrary prose. A line marker with a nonempty description is a deliberate report. Keep structured dogfood and requirement evidence unchanged. Document the marker syntax in the existing milestone skill; no model classification or safety policy changes are needed.

Keep the Markdown project memory file as the repository backlog source. The handoff references that file when it has active task entries and names the selected item in its exact next action. It does not copy all issue text or infer approvals. This avoids a new store, schema or GitHub write. The handoff artifact schema remains backward compatible. A project-specific requirements note is generated from this reviewed delivery record, while the record itself supplies the requirement, design, user-story, acceptance, test and traceability content needed before code. No new ADR, UX mockup, data migration or deployment plan is applicable: this is a bounded CLI interpretation and documentation-discovery change with no external user interface.

## Implementation instructions and readiness

Inspect `KARAKANA.md`, the current handoff, `docs/engineering-process.md`, `skills/karakana-self-improvement/SKILL.md`, `skills/next-milestone-decision/SKILL.md`, `karakana/milestones/decision.py`, `karakana/handoffs/builder.py`, project memory, relevant tests and the two reproduced milestone artifacts. Verify the branch and upstream before editing. Then:

1. Add focused regressions for historical identifiers, negation/closed phrasing, explicit note blockers, structured dogfood blockers, and project-scoped handoff backlog discovery; confirm the new tests fail for the observed behavior.
2. Make the smallest code changes to note priority handling and handoff backlog reference; update the milestone skill's note syntax and populate the project development backlog with evidence and bounded next actions.
3. Run focused tests. Use the safe allowlisted dogfood command and requirements workflow on the current project, inspect their artifacts and classify warnings. Run the required broader regression and validation gates, then review the diff and append actual outcomes below.
4. Commit on the task branch. Publish or merge only under the applicable external-write authority; preserve runtime artifacts outside the commit. Refresh and validate the append-only handoff.

Before implementation, the code path, governing instructions, observed failure, chosen parser grammar, project backlog path, test strategy and rollback are explicit. Revert the reviewed commit if the behavior is rejected; append-only runtime records remain intact. The material risk is an incorrectly missed or invented planning blocker, so positive and negative regression cases and structured-priority preservation are required.

## Verification and delivery outcome

The parser now recognizes only full note lines with a nonempty `P0:` or `P1:` description, and it carries that description into the blocker. Active items in the selected project memory's `open-issues.md` are linked from the handoff's state, inspect-first list and artifact references. The two affected skills and their deterministic eval expectations document this behavior. The development backlog has stable IDs, evidence, acceptance and next actions. The source changes are in `karakana/milestones/decision.py`, `karakana/handoffs/builder.py`, the two skills, two eval cases, two test files, project memory and this record.

The new regressions failed against the old behavior and passed after the fix. Focused handoff and milestone suites passed **48/48**. The full `pytest -q` gate passed **707/707**. `karakana memory validate --project karakana`, `karakana skill validate-all` and `karakana eval run` passed; the eval report `20261001-154812-eval-e0fd0e` contains **173 passed, 0 failed, 0 warnings**. `karakana skillpack validate-all` exited successfully with existing warnings for absent `billing`, `msc-research` and `nhrdm` memory paths; KDX-07 records their review. The CLI milestone check `20261001-154711-milestone-b40f27` found no note blocker for `P06`, negated P0/P1 and closed P1 prose.

Fresh full dogfood `20261001-154355-dogfood-c4944f` completed all ten safe commands, produced five medium findings and no P0/P1 item. Doctor's missing optional credentials are expected in this offline worktree. The workspace status and validation warnings arise from sibling paths resolved under `/tmp`; the status warning is real, although its finding captures only the `## Warnings` heading. Skillpack validation found the three absent memory paths above. The eval command itself passed 173/173 with `warnings: 0`, but dogfood incorrectly marked that line as a warning; KDX-05 covers the classifier. The generated dogfood backlog is triage output, not release authorization.

Requirements run `20261001-154449-req-565169` passed structural readiness. Semantic inspection rejected its generated PRD as task authority: its stories and functional requirements describe the generic requirements generator rather than the milestone parser and handoff backlog. This task-specific record provides the project-specific requirements and acceptance evidence for this slice. KDX-06 tracks the separate readiness defect; no issue draft was published.

The remaining material risks are the generic requirements readiness false positive, noisy dogfood warnings, and unreviewed external integration. The local branch awaits pull request review. No remote write, deployment, live model call, or protected-branch change occurred. The recommended next development task after integration is **KDX-05**, a focused dogfood warning-classifier correction; inspect its source and fixtures, add zero-count and real-warning regressions, then verify with focused tests and a safe dogfood rerun. GPT-6 Sol with high reasoning is suitable because the classifier affects control-plane evidence; a fresh conversation would help keep that slice bounded.
