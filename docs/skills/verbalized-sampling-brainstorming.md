# Verbalized-Sampling Brainstorming

## Purpose

Translate Verbalized Sampling into a practical, evidence-aware Karakana technique for brainstorming and decision support before requirements and issue generation.

## Paper Summary

[Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity](https://arxiv.org/abs/2510.01171) by Zhang et al. identifies typicality bias in preference data as a driver of reduced output diversity after alignment. It proposes a training-free distribution-level prompt: ask a model for multiple responses and corresponding probabilities rather than one response or an unweighted list.

The paper reports improved diversity across creative writing, dialogue simulation, open-ended QA, and synthetic-data generation without a measured factuality or safety loss in its evaluated settings. It also reports two practical limits: generating several candidates costs more tokens and latency, and less capable models may gain less or lose quality under the structured probability task.

Karakana's adaptation is an inference-time option-generation heuristic. It is not a claim that model-verbalized probabilities are calibrated or that the paper directly validated software architecture decisions. Final selection uses a separate transparent multi-criteria model and sensitivity analysis documented in [Scientific Decision Ranking](scientific-decision-ranking.md).

## Why Direct Brainstorming Can Collapse

A direct request for "the best option" encourages an aligned model to produce the most typical, familiar, or conventionally preferred response. Asking for a plain list improves breadth but can still flatten alternatives into a uniform list with no view of plausibility or uncertainty. It also anchors evaluation on the first plausible answer.

Distribution-level prompting forces the model to expose several modes, including lower-frequency but credible options. A separate decision step then evaluates those options against evidence and constraints.

## Karakana Adaptation

Karakana uses two stages:

1. **Explore:** generate 4-7 materially distinct options with relative decision weights that sum to 1.0, rationales, risks, cost, reversibility, evidence needs, implementation fit, and uncertainty flags.
2. **Decide:** define a criterion matrix, score every option consistently, calculate normalized score shares, and test ranking sensitivity before selecting an option or hybrid.

The verbalized probabilities are explicitly uncalibrated. They help reveal the model's option distribution; they do not establish objective likelihood, correctness, consensus, or authority. The later MCDA decision weights are normalized score shares and are not probabilities. Project docs and human decisions remain authoritative.

## Prompt Pattern

```text
Decision question: <neutral decision question>

Constraints and evidence:
- <project contract, ADR, user intent, current behavior, test evidence>

Generate 4-7 materially distinct plausible options. Assign relative
probability/confidence weights summing to 1.0. For each option explain why it
might be right, its risks, implementation cost, reversibility, evidence needed,
and implementation fit. List assumptions and uncertainty flags.

Treat the verbalized probabilities as uncalibrated generation metadata. Then
define a criterion matrix for implementation cost, risk, reversibility,
alignment with project docs, alignment with user intent, evidence strength, and
unknowns. Show scores, normalized score shares, sensitivity results, and
rejected alternatives. Do not label the decision weights as probabilities.
```

## Output Schema

```markdown
# Verbalized-Sampling Brainstorm

## Decision Question

## Constraints and Evidence

## Option Distribution

| Option | Probability | Why It Might Be Right | Risks | Cost | Reversibility |
|---|---:|---|---|---|---|

## Uncertainty Flags

## Recommended Decision

## Rejected Alternatives

## Next Action
```

## Decision Rule

The highest-weight option is not automatically the recommendation. Evaluate every candidate against:

1. probability/confidence weight;
2. implementation cost;
3. risk and unsafe failure modes;
4. reversibility and learning value;
5. alignment with project docs and ADRs;
6. alignment with explicit user intent;
7. strength of inspected evidence;
8. unknowns that could change the result.

Prefer bounded and reversible learning when evidence is weak. Prefer stronger evidence and review as harm, cost, or irreversibility grows. Reject any option that violates a safety rule regardless of its weight.

## When To Use

- Before requirements elicitation when the goal admits several valid scopes.
- During elicitation after documents have narrowed but not resolved the options.
- Before PRD generation to select one scope and make non-goals explicit.
- For architecture, workflow, research-method, prioritization, or prototype choices where alternatives matter.
- For generating ranked hypotheses, provided each will later be tested against evidence.

## When Not To Use

- Simple factual questions or deterministic validation.
- Straightforward implementation with an approved decision.
- High-risk decisions without independent evidence and human review.
- Situations where extra candidates and tokens add cost but no decision value.
- As a mechanism to rationalize prohibited, destructive, or unsafe behavior.

## Safety Rules

- Verbalized probabilities are uncalibrated generation metadata.
- MCDA decision weights are normalized score shares, not probabilities.
- Do not hide uncertainty or imply calibration.
- Do not choose the most familiar option by default.
- Do not use diversity to justify unsafe actions.
- Require evidence and human review in high-risk domains.
- Preserve dry-run, approval, secret, deployment, data, and external-write gates.
- Do not let optional model review overwrite deterministic facts or human acceptance.

## Examples

### Pre-PRD scope choice

Instead of asking "What dashboard should we build?", compare status-only, bounded action, full workflow, admin-only, and CLI-only surfaces. Weight each, then select using current dashboard behavior, slice non-goals, operator needs, cost, and reversibility.

### Architecture choice

Compare extending an existing module, adding a focused module, using an adapter, running a reversible spike, and deferring the decision. A lower-weight spike may be recommended when it cheaply resolves the dominant unknown.

### Research review

Generate several plausible topic-suitability judgments and uncertainty flags. Store the distribution as assistive evidence, keep deterministic curriculum extraction unchanged, and require a human decision before promotion.

## Use Before PRD and Issues

1. Run `requirements-elicitation` from the user goal and project docs.
2. Use this skill only for unresolved multi-option decisions.
3. Record the selected option, rejected alternatives, and uncertainty in the elicitation result.
4. Save the reviewed result and pass it to `karakana requirements prd --from-file`.
5. Generate stories and vertical issues only after PRD review; then run `requirements ready`.
