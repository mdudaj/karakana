# Release notes from delivered evidence

Inspect the actual released/candidate baseline, merged changes and observed check or
release records, according to the project's definition of delivered. Do not infer a
release from a commit, planned feature, successful build or draft document.

For each note state the audience, changed behavior and practical impact. Include
compatibility/migration needs, known limits and support references where relevant.
Link the release/source artifact and scoped evidence. Group changes by useful reader
categories instead of copying raw commits. Match the project's version/date convention.

A plan item remains in the release plan until supported as delivered. If evidence is
absent, record the missing observation and omit the delivered claim; a labelled
preview is planned communication, not a delivered Release Notes table row. A release
note must not imply production deployment or user acceptance unless separately evidenced.

Example wording shape: what the user can now observe; where it applies; any action
needed; what is still limited; source/candidate and evidence. Keep implementation
internals only when they affect a user/operator decision. Use real observations,
not invented dates, metrics, reviewer names or assurance.

Regenerate notes when scope changes; preserve previously communicated history and
explain corrections. Existing changelog conventions remain project-specific.
Basis: [research/plan](../../../docs/skills/engineering-artifact-catalogue/PLAN.md),
S25/S26, public primary guidance, and scoped project release facts.
