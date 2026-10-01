# KDX-05 dogfood warning classification: delivery record

Status: implementation authorized by the user's 2026-10-01 instruction to execute the next proposed development task after PR #21 merged. This record covers the task branch only; it does not authorize a new remote write or merge.

## Evidence and outcome

Full dogfood run `20261001-154355-dogfood-c4944f` marked `eval run` as a warning for `Cases: 173, passed: 173, failed: 0, warnings: 0`. The same run stored only `## Warnings` as evidence for workspace status, although its output has a real `- Project path missing: crdb-mel` item beneath that heading. `karakana/dogfood/runner.py` currently selects lines by the word `warning` and treats truncated excerpts as complete lines. The doctor command has optional credential warnings, which existing tests expect to remain informational.

The outcome is command results that reflect actual warning messages: zero-count summaries stay passed; genuine warning items retain their text and produce warning status; informational optional credentials do not create findings. No allowlist, command execution, safety gate, or report schema change is needed.

## Acceptance and method

1. For successful eval output with `warnings: 0`, the result has status `passed` and an empty warnings list. A positive count or explicit warning line still has warning status.
2. `## Warnings` and `Warnings:` are section labels, not evidence. A substantive bullet under either label is captured verbatim, while `- None` and `No warnings` are ignored.
3. Doctor's optional `github_token`, `gh_token`, OpenAI and Anthropic credential warnings are informational; a noncredential warning remains visible. A shortened excerpt must not turn a cut-off credential line into a fabricated warning.
4. Existing safe command execution and real failure handling remain intact. Focused runner/findings tests, full pytest and eval suites, a safe targeted dogfood rerun, diff review and protocol completion verify the result.

The design is a small line-oriented parser in `karakana/dogfood/runner.py`: recognize warning sections and their items, ignore explicit zero-count summaries and status headings, keep direct warning lines, and select evidence from full redacted command output while preserving bounded stored excerpts. Update `tests/test_dogfood_runner.py` with red/green regressions. Refresh `ubongo/projects/karakana/open-issues.md` with the verified local state after tests. Rollback is a revert of this task's reviewable commit. No PRD, ADR, migration or UX artifact is applicable to this internal CLI evidence-classification fix.

## Implementation and verification

The new tests first reproduced four failures: zero-count eval output, a workspace warning section with lost message, optional doctor status, and a cut-off optional credential line. A safe full dogfood run after the first fix exposed a fifth false positive from `warning` inside a branch and filename; a focused regression reproduced it before the parser was narrowed. The focused runner/findings suite then passed **15/15**. The full `pytest -q` gate passed **714/714**; `karakana eval run` passed **173/173** with zero warnings, and `karakana skill validate-all` passed.

Safe full dogfood run `20261001-160648-dogfood-b3997b` exercised ten commands. `eval run`, `doctor`, and `workspace status` all passed without fabricated warnings. `skillpack validate-all` and `workspace validate-all` still report real absent project paths with their concrete messages. `dogfood analyze` generated two medium findings for those existing configuration gaps; KDX-07 tracks them. No secrets, live model calls, deployment or external GitHub write were used.

The branch change consists of `karakana/dogfood/runner.py`, focused tests, this record and project backlog. Review the diff for warning-message preservation and redaction, then publish a PR only with applicable GitHub write authority. The next development task after integration is **KDX-06**, the project-specific requirements readiness check. GPT-6 Sol with high reasoning is recommended because it changes a control-plane readiness decision; a fresh conversation would help keep that task bounded.
