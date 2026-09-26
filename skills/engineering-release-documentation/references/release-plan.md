# Release candidate and assurance plan

Record candidate scope/version scheme, source baseline/revision and intended target.
Use the project versioning convention; do not assume every release uses SemVer.
Separate target date/forecast from actual publication, deployment and acceptance.

List actual readiness evidence and gaps: accepted scope, required checks/reviews,
known defects/risks, compatibility/data migrations, support, rollout and recovery.
For each gate record source/revision/environment/observation/owner, or explicitly
Not run/Blocked/unconfirmed. A green CI badge alone does not establish release authority.

Describe rollout, stop/recovery conditions and how post-change behavior would be
checked under the existing release/runbook process. Do not claim backup restoration,
monitoring, training or operator readiness without actual scoped evidence. Link
sensitive operational configuration without reproducing secrets.

Keep candidate verification, merge, publication, deployment and user acceptance as
separate facts; none implies the next. The release plan contains planned scope.
Delivered release notes require actual scoped observation. Operational approval is
the project's existing decision, not a workbook cell or parser result.

Tailor the pack to the audience and risk; preserve blockers in all share views.
Missing evidence is a release-review finding, not permission to fill defaults.
Basis: [research/plan](../../../docs/skills/engineering-artifact-catalogue/PLAN.md),
S19/S20/S24–S27 and the project's release protocol/runbooks.
