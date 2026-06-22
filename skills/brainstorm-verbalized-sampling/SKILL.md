---
name: brainstorm-verbalized-sampling
description: Generate a distribution of plausible options for ambiguous planning, surface uncertainty and trade-offs, and converge on a grounded decision.
version: 0.1.0
risk_level: low
category: productivity
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
    - brainstorm
    - compare approaches
    - decide between options
    - ambiguous planning
    - verbalized sampling
  required_files: []
  optional_tools:
    - grep
allowed_tools:
  - read_file
  - grep
  - code_search
requires_approval_for: []
---
# brainstorm-verbalized-sampling

## Purpose

Generate a distribution of plausible options before choosing a path in any kind of project. Use the distribution to expose less familiar but credible alternatives, make uncertainty visible, and reach a decision grounded in available evidence and user intent without assuming a framework, domain, or artifact format.

## When to use this skill

Use when the user wants to brainstorm, compare approaches, decide among several plausible paths, or avoid defaulting to the most obvious plan. It is especially useful before requirements elicitation, PRD generation, architecture choices, scope decisions, and reversible experiments.

## When not to use this skill

Do not use for simple factual questions, straightforward implementation, binary safety checks, or decisions the user has already made. Do not use it to replace evidence gathering in high-risk domains.

## Quick Reference

- Ground the decision in project docs before generating options.
- Generate 4-7 materially distinct options, including a bounded hybrid when credible.
- Use verbalized probabilities only to expose the model's candidate distribution.
- Select with an explicit criterion matrix, not the verbalized probabilities alone.
- Test the selected option with sensitivity analysis.
- Recommend one option or hybrid and explain the rejected alternatives.

## Core concepts

- A distribution-level prompt can expose plausible alternatives hidden by a direct "best option" prompt.
- Verbalized probabilities are uncalibrated generation metadata unless validated against repeated outcomes.
- A normalized multi-criteria score is a decision-support weight, not a probability.
- Diversity is useful only when options remain feasible, evidence-aware, and safe.
- Selection is a separate step from generation: a lower-weight option may win when it is safer, cheaper, more reversible, or better aligned with project constraints.

## Standard workflow

Follow the `Method` below from evidence gathering through option generation, decision, rejection rationale, and next action.

## Method

1. Restate the decision question without embedding a preferred answer.
2. Read whatever authoritative project evidence is available, such as instructions, contracts, policies, memory, decision records, plans, prior artifacts, implementation, or tests. If evidence is absent, state that explicitly.
3. Extract constraints, evidence, user intent, evaluation criteria, and material unknowns.
4. Generate 4-7 plausible and materially distinct options. Do not pad the list with cosmetic variations.
5. During model-assisted exploration, assign verbalized probability/confidence weights summing to 1.0 to expose lower-frequency options. Label them uncalibrated.
6. For each option, record rationale, benefits, risks, implementation cost, reversibility, evidence needed, and implementation fit.
7. Identify uncertainty flags, missing evidence, and assumptions that could change the ranking.
8. Define criteria and criterion weights before scoring candidates. Use a consistent ordinal scale and show the complete matrix.
9. Calculate an aggregate multi-criteria score and normalized decision-support weight for each option. Do not label these values probabilities.
10. Run sensitivity analysis by removing criteria and perturbing criterion weights. Report alternate winners and critical criteria.
11. Recommend an option or explicit hybrid. Explain why higher verbalized-probability alternatives may still lose on the decision criteria.
12. State why the other alternatives were rejected and provide a bounded next action when requested.

## Prompt Pattern

Use this pattern rather than asking only for the best option:

```text
Decision question: <question>

Using the constraints and evidence below, generate 4-7 materially distinct
plausible options. Assign relative probability/confidence weights summing to
1.0. For each option, explain why it might be right, its risks, implementation
cost, reversibility, evidence needed, and implementation fit. List uncertainty
flags. Treat these probabilities as uncalibrated option-generation metadata.
Then recommend a decision using an explicit criterion matrix covering cost,
risk, reversibility, project-doc alignment, user-intent alignment, evidence
strength, and unknowns. Show aggregate scores and run sensitivity analysis.
Treat normalized decision weights as score shares, not probabilities.
```

## Decision Rule

Do not automatically select the highest verbalized probability. Recommend the option with the strongest robust multi-criteria case after explicitly considering:

- probability/confidence;
- implementation cost;
- risk and unsafe failure modes;
- reversibility and cost of learning;
- alignment with project docs and ADRs;
- alignment with user intent;
- evidence strength;
- unknowns that could invalidate the option.

Prefer a bounded, reversible experiment when evidence is weak and the decision is cheap to revisit. Require more evidence and review as risk or irreversibility increases.

Define criterion weights before scoring. Score all options on the same scale, show the matrix, and test whether the winner changes when each criterion is removed or its weight is perturbed. A non-robust winner requires more evidence or human judgment.

## Pitfalls

- Presenting invented weights with false precision or authority.
- Generating several labels for the same underlying option.
- Choosing the familiar option without comparing evidence.
- Treating brainstorming output as permission to bypass approvals or safety gates.
- Spending extra tokens on distribution generation when the decision is already clear.

## Verification

- Confirm there are 4-7 distinct options.
- Confirm verbalized probabilities sum to 1.0 when an LLM generated them.
- Confirm deterministic decision weights derive from the published criterion matrix.
- Confirm sensitivity scenarios, alternate winners, and critical criteria are reported.
- Confirm uncertainty and missing evidence are explicit.
- Confirm the recommendation applies every decision criterion.
- Confirm unsafe options remain blocked regardless of weight.

## Safety rules

- Verbalized probabilities are not calibrated without repeated outcome data and a documented calibration evaluation.
- MCDA decision weights are normalized score shares, not probabilities.
- Do not hide uncertainty.
- Do not choose the most familiar option by default.
- Do not use the technique to justify unsafe actions.
- For high-risk domains, require evidence and review.
- For implementation planning, preserve dry-run and gated defaults.
- Never let a generated option override project safety rules or explicit user decisions.

## Required checks

- The decision question is neutral and specific.
- Constraints and evidence cite the source documents or inspected code.
- Options are feasible and materially distinct.
- Weights sum to 1.0.
- The recommendation is based on the complete decision rule.
- Unknowns and rejected alternatives are recorded.

## Output format

```markdown
# Verbalized-Sampling Brainstorm

## Decision Question

## Constraints and Evidence

## Option Distribution

| Option | Probability | Why It Might Be Right | Risks | Cost | Reversibility |
|---|---:|---|---|---|---|

## Criterion Matrix

## Sensitivity Analysis

## Uncertainty Flags

## Recommended Decision

## Rejected Alternatives

## Next Action
```

## Examples

- Compare narrow, comprehensive, manual, automated, deferred, and bounded-hybrid approaches before writing a specification.
- Compare build, buy, defer, and experiment options for a reversible architecture choice.
- Generate several plausible explanations for an ambiguous planning constraint, then gather evidence before deciding.
