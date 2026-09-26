# Karakana Overview

Karakana is a multi-project agent harness for durable memory, skills, deterministic
task routing, planning/coding prompts, traceable delivery and reviewable improvement.

Current process: `docs/engineering-process.md`; model policy:
`docs/gpt-6-routing.md`; continuation policy: `docs/cost-aware-continuation.md`.
The CLI includes protocols, artifact checks, handoffs, evals and opt-in execution.
Instructions and presence checks support disciplined work; they do not guarantee
agent compliance or grant approval for external actions.

Known follow-up: isolate test runtime artifacts and project provenance in handoff
recovery. Verify recovered references before use. The agent guide's initial
milestones must not be treated as an up-to-date implementation inventory.
