# Copy-ready implementation instructions

A later implementer should know what to inspect, what governs the change, what to do
and how to verify. Record current source revisions and the relevant files/interfaces,
requirements/decisions, skills and actual unresolved findings. Use the existing issue
workflow when it already owns the task; do not generate a second set of native IDs.

For each bounded task include purpose, ordered steps, dependencies, acceptance/checks
(command and expected observation), applicable authority and recovery. Prefer small
reviewable steps; name the next exact action. Leave choices open where multiple valid
implementations satisfy the contract, rather than prescribing incidental code.

Build verification from acceptance: use regression reproduction for real bugs and
meaningful tests/evals/manual observations. Run focused checks while iterating, then
the required broader gate. A plan names unperformed checks without reporting them as
passed. A test command alone is not evidence of its outcome.

For risky changes record preconditions, stop conditions and recovery/revert evidence.
Drafting does not authorize destructive operations, migrations, authentication,
permission changes, live models, GitHub writes or deployment. Preserve the project's
existing approvals; do not add speculative approval questions for routine in-scope
reversible edits already authorized.

Finish with remaining work and continuation. A proposed implementation plan is not
execution. Inspect existing artifacts first; avoid duplicated plans/research when
current evidence already satisfies the stage. Basis:
[research/plan](../../../docs/skills/engineering-artifact-catalogue/PLAN.md), L01/L05 and
[engineering lifecycle](../../../docs/engineering-process.md).
