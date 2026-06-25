# ADR 0004: Prefer Copilot Max GitHub Inference for Planning Roles

Date: 2026-06-25

## Status

Proposed

## Context

Karakana routes work across lightweight language, planning, implementation, review, and high-risk engineering roles. The harness needs to use tokens efficiently while keeping each role focused on the kind of work it is meant to perform.

GitHub's Copilot billing documentation states that Copilot usage consumes input, output, and cached tokens, and that paid Copilot plans include GitHub AI Credits with model-specific token pricing. GitHub Models documentation also describes model catalog, prompt management, and eval support for comparing model behavior. That means Karakana should make route purpose and token-budget intent explicit, not just provider and model names.

References:

- https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing
- https://docs.github.com/en/github-models
- https://docs.github.com/en/copilot/reference/ai-models/supported-models

## Decision

Karakana will treat Copilot Max and GitHub inference as the default lane for non-mutating context work:

- Issue triage and simple summaries use the `triage_summarizer` role with a `small` token budget.
- Documentation, changelog, release-note, and cleanup prose use the `documentation_writer` role with a `small` token budget.
- Routine bounded planning, requirements reasoning, reflection, action extraction review, and low-risk assessments use the `planner` or `assessment_reviewer` roles with a `standard` token budget.
- Non-mutating repository research, evidence review, and trace reflection use the `researcher` or `reflection_reviewer` roles with a `standard` token budget.
- Consequential planning, architecture review, framework design, protocol/workflow changes, skill design, and system-impact assessment use the `deep_planner` role with a `large` token budget before mutation.
- Model routing, safety policy, high-risk planning, and cross-project architecture use the `principal_planner` role with a `reserved` token budget before mutation.
- Routine implementation uses the `routine_implementer` role with a `standard` token budget.
- Test generation and bounded task drafting use the `test_designer` and `task_author` roles with a `standard` token budget.
- Refactoring, framework implementation, and non-routine repository edits use the `serious_implementer` role with a `large` token budget.
- CI failure analysis and repository-aware PR review use the `ci_analyst` and `code_reviewer` roles with a `large` token budget.
- Authentication, authorization, billing, migrations, workflow state changes, production-risk review, and stuck/high-risk review use the `principal_reviewer` role with a `reserved` token budget.

Routes must expose role, token budget, token policy, and escalation policy in CLI output and traces. Agents should use those fields to avoid spending high-cost implementation tokens on work that should be summarized, classified, planned, or reviewed first through GitHub inference.

## Consequences

- Future route changes can be tested against role and budget intent, not only model names.
- Token-heavy Codex routes remain available for implementation and high-risk work, but require a clear escalation reason.
- GitHub inference remains preferred for routine planning and requirements discussion, while consequential or high-risk planning escalates before implementation. Live model calls remain explicit and opt-in.
- Traces become easier to audit for route misuse and unnecessary escalation.

## Verification

- Router tests assert role and token-budget metadata for planning, docs, implementation, and high-risk routes.
- CLI tests assert `karakana model route` prints and emits role policy fields.
- Model-routing evals include a Copilot Max planning budget case.
- Safety-policy protocol artifacts must record approval and verification before this ADR is accepted.
