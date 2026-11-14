# Narrative content checker M1: continuation

CT01-CT08 convention/templates are integrated through PR #36 (`f2319cc`), and
PI01-PI08 parser integrity through PR #37 (`fc93fbc`). Preserve those completed
slices. The [parent roadmap](DRAFTING-CONVENTIONS-2026-11-13.md) retains history;
the current [bounded plan and M1 results](CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md)
govern continuation alongside the accepted
[requirements](CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md) and
[design](CONTENT-PROFILE-DESIGN-2026-11-13.md).

M1 is implemented, locally verified and owner-accepted on
`feat/engineering-content-checker-m1-20261114`. Its final gate passed **885 tests**
(67 new) and **186 deterministic evals**, zero warnings, plus actual installed-wheel,
CLI, skill/skillpack and sixteen protected-source byte-preservation controls.
These are historical verified-source receipts; reconcile current source/CI before
reuse. No native Windows installation qualification or standards certification
is claimed; actual LF/CRLF bytes were tested.

The module `karakana.tools.engineering_content` and
[usage guide/default context](content-checks/README.md) provide explicit M1 standard
requirements/system-design narrative checks, strict raw-table consumption, content/
reference diagnostics and immutable current-run reports. The optional content/dev
parser is pinned to4.3.0. Review remains required; gaps/readiness/acceptance are
separate. Advanced context mappings, context0.2/links and saved-report verification
are explicitly unsupported. P02 structural/native-binding/export behavior remains
unchanged; narrative checking does not add P02 export support or automatic gates.

First inspect current `main`, the M1 source/tests and the branch PR state. The owner
clarified **“squash merge, thats approved means”**: M1 commit/push, PR publication
and validated squash integration are authorised; do not ask for that approval
again. If its PR is pending, finish this integration task with current CI and an
expected-head guard. If it is merged, carry the squash/tree/parent/release receipt
forward and use the latest handoff instead of restarting M1 implementation.

After M1 squash integration and release checks, the next bounded issue is the M2
explicit-reference mapping amendment. The accepted design promises source-cell/
target mappings but omits a two-endpoint field. The plan proposes optional `links`
in context0.2, each edge with existing `from`/`to` Locators, preserving0.1. Obtain
the owner's agreement on that exact amendment before activating M2; it was not
approved merely by M1 acceptance/integration. M2 then adds actual tailored sources,
open-item/claim evidence mappings and recomputed report verification. Automatic
selection/enforcement, remaining templates/exports, pilot and Jovina remain later.

Follow repository instructions, load/expose the latest handoff summary and keep
task/project boundaries. Loading context grants no fresh deployment, model-call
or client-revision authority. No app-server connection is needed. Prefer GPT-6 Sol
high for integrity review; a fresh conversation benefits the completed boundary.
