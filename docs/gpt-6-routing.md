# GPT-6 task routing — decision and delivery plan

## Requirements

Preserve difficulty/risk routing and explicit execution approval. Replace active
Codex defaults, not historical records or unrelated API-provider defaults.
Use GPT-6 Sol for control-plane judgment, Luna for bounded execution, and retain
GPT-5.6 as explicit fallback. Register Astra without selecting it automatically.

## Evidence and architecture

Official guidance checked 2026-09-26:

- [Models](https://learn.chatgpt.com/docs/models): Sol for complex coding and
  agentic workflows; Luna for focused work; Astra for the most demanding reasoning.
- [Agent model configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents):
  starting effort Sol medium, Luna high, Astra low. No maximum/Ultra defaults.
- [Pricing](https://learn.chatgpt.com/docs/pricing): Astra's standard token-credit
  rates are five times Sol's. Actual account limits are not determined by rates alone.

Policy decisions (not claims of benchmark superiority):

| Work | Model | Reasoning |
| --- | --- | --- |
| Control-plane judgment, architecture, coordinated changes, review | GPT-6 Sol | medium |
| High-risk auth, billing, migration, production review | GPT-6 Sol | high |
| Bounded research, summaries, routine edits/tests | GPT-6 Luna | high (documented starting setting) |
| Exceptional unresolved problems / second opinion | GPT-6 Astra | low initially; explicit override only |

Python owns routing, approvals and artifact checks. A controller is a task role,
not an always-running extra agent. Two failed diagnostic attempts on Luna route
to Sol; stuck Sol work recommends a human-reviewed replan or explicit Astra review,
not automatic fan-out. Availability fallback is not capability escalation: choose
5.6 Luna for Luna-class work, 5.6 Sol for Sol-class work only after availability
confirmation. Do not silently downgrade risk-sensitive work or retry paid calls.

## Implementation and acceptance

Inspect router, escalation, safety warnings, providers/config, Codex handoff and
executor, project skillpacks and active guidance. Centralize model/effort/fallback
metadata; preserve manual overrides and mock defaults. Propagate reasoning into
structured task launches and handoffs. Update tests and active eval expectations;
retain legacy catalog entries and fixtures specifically exercising old overrides.

Tests must establish routine vs control-plane vs risk routing; Astra is never a
default; 5.6 Luna is not a principal model; project overrides cannot leave bundled
defaults obsolete; legacy overrides remain accepted; no automatic live calls;
explicit executor uses model and effort and reports nonzero exit as failure.

Validation: focused routing/handoff tests, full pytest, skills/skillpack validation,
deterministic evals, diff review and CI. Correct the already-known Material eval
false positive without weakening its actual accessibility requirement so merge
does not bypass a failing gate. No deployments or external model calls.

## Rollback

Revert this PR to restore earlier defaults. No database migration or secrets change.
Old handoffs remain readable. A selected interactive session model is never
changed by writing routing config. Upgrade/reload the harness in other checkouts
after merging and start a fresh project-specific conversation.

## Delivery verification — 2026-09-26

- 551 tests passed; 144 deterministic evaluations passed.
- Skills validated; skillpacks validated with pre-existing missing-memory warnings
  for billing, msc-research and nhrdm. `git diff --check` passed.
- Reviewed default routes, overrides, risk warnings, reasoning propagation, legacy
  compatibility, explicit subprocess launch and failure reporting. Launch tests use
  mocks; no live model call or account availability probe was performed.
- Active evaluation model expectations were refreshed without removing safety
  assertions. The Material eval now explicitly requires “Do not rely on color
  alone” instead of rejecting its own accessibility guidance.
- Existing handoff improvements are included in this delivery. App code and UAT
  artifacts are excluded. Interactive sessions still require deliberate selection.

Residual follow-up: isolate tests that write runtime traces into the source
checkout; those traces can shadow a task's latest protocol. Use the explicit task
protocol check for delivery evidence. Model capability comparisons remain policy
choices until measured on representative project tasks; no performance guarantee.
