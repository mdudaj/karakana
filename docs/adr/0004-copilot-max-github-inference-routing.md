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

- Issue triage, documentation, changelog, and simple summaries use the `triage_summarizer` role with a `small` token budget.
- Planning, architecture review, reflection, skill design, requirements reasoning, and action extraction review use the `planner` role with a `standard` token budget.
- Routine implementation, test generation, and Codex task drafting use the `routine_implementer` role with a `standard` token budget.
- CI repair, refactoring, framework implementation, and repository-aware PR review use the `serious_implementer` role with a `large` token budget.
- Authentication, authorization, billing, migrations, workflow state changes, cross-project architecture, and stuck/high-risk review use the `principal_reviewer` role with a `reserved` token budget.

Routes must expose role, token budget, token policy, and escalation policy in CLI output and traces. Agents should use those fields to avoid spending high-cost implementation tokens on work that should be summarized, classified, planned, or reviewed first through GitHub inference.

## Consequences

- Future route changes can be tested against role and budget intent, not only model names.
- Token-heavy Codex routes remain available for implementation and high-risk work, but require a clear escalation reason.
- GitHub inference becomes the preferred place for planning and requirements discussion while still keeping live model calls explicit and opt-in.
- Traces become easier to audit for route misuse and unnecessary escalation.

## Verification

- Router tests assert role and token-budget metadata for planning, docs, implementation, and high-risk routes.
- CLI tests assert `karakana model route` prints and emits role policy fields.
- Model-routing evals include a Copilot Max planning budget case.
- Safety-policy protocol artifacts must record approval and verification before this ADR is accepted.
