# Karakana Overview

Karakana is a multi-project agent harness for durable memory, skills, deterministic
task routing, planning/coding prompts, traceable delivery and reviewable improvement.

Current process: `docs/engineering-process.md`; model policy:
`docs/gpt-6-routing.md`; continuation policy: `docs/cost-aware-continuation.md`.
The CLI includes protocols, artifact checks, handoffs, evals and opt-in execution.
Instructions and presence checks support disciplined work; they do not guarantee
agent compliance or grant approval for external actions.

Handoff project boundaries and test-runtime isolation are implemented; see
`docs/handoff-provenance.md`. Legacy recovered artifacts remain intact and must
be verified before use. Bind refresh to the task trace and omit stale automatic
recovery when supplying verified current state. The agent guide's initial
milestones must not be treated as an up-to-date implementation inventory.
