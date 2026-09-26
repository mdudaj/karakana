# Requirements and PRD authoring

Use a reviewed intent seed or accepted source requirement. If a missing choice
would alter scope/safety/acceptance, use elicitation; otherwise state the assumption
and keep drafting within authorization. Do not ask for facts the repository holds.

A useful PRD narrative answers: what problem, whose work, what outcome, current
context, scope/non-goals, constraints and uncertain decisions. Reuse existing
project language and structure. Group needs as Business, Stakeholder, Solution
or Transition when the shared export convention applies; grouping is a local
convention, not standards certification.

For each requirement record a stable ID, singular verifiable statement, rationale,
source, owner/status and priority basis. Separate needs from a preferred design.
Avoid “fast”, “secure” or “easy” without a scoped measure/method: define the workload,
environment, threshold and observation that would resolve the claim. An unavailable
threshold is an open acceptance decision, not permission to choose a convenient one.

Record Proposed Priority separately from Agreed Priority. Unknown owner/priority
is unconfirmed. Agreement requires actual authority/evidence for that baseline.
Resolve contradictions explicitly rather than blending older and newer sources.

Existing Karakana PRD JSON owns its native fields. Inspect the existing schema/store
before proposing changes; import references and persistent reviewed bindings using
P02. Do not hand-edit generated engine Markdown, generate new native objects merely
for export, or turn a new documentation skill into a second PRD generator.

For export use the exact Requirements/Sources headers in the shared template and
scalar frontmatter. Review meaning separately from parser success. Basis:
[research/plan](../../../docs/skills/engineering-artifact-catalogue/PLAN.md),
S01/S07/S08/S11/S12 and local L02; full paid standards were not read.
