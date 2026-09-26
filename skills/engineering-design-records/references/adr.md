# Decision records

Use an ADR for a consequential choice future maintainers would otherwise have to
rediscover. Reuse a current accepted decision if it still governs. A tiny mechanical
change may need a compact rationale in an existing record rather than a new ADR.

Retain context/problem, decision drivers and constraints, plausible alternatives,
selected direction, rationale/trade-offs, positive/negative consequences and follow-up
conditions. Describe why rejected alternatives were plausible and why they lost.
Do not invent a list merely to justify a choice already made without evidence.

Decision status is Proposed until actual decision-owner authority is evidenced.
Accepted needs source revision, scoped reviewer/authority, decision/time/evidence;
metadata or structural validation cannot supply that authority. Containing document
status remains distinct. Do not mark an old decision superseded without linking the
replacement and preserving the old reasoning/history.

A changed decision gets its own revision or a superseding record according to project
conventions. Explain changed drivers and consequences; link affected requirements,
contracts, risks and migration/recovery. Preserve what readers relied on earlier.

Full reasoning stays in Markdown. ADRs/ADR Source Sections tables are summaries or
labelled excerpts linked to explicit source anchors; they do not replace alternatives
and consequences. Review the complete source before acceptance.

See the [synthetic design example](../examples/design.md). Basis:
[research/plan](../../../docs/skills/engineering-artifact-catalogue/PLAN.md), S15–S18,
and ADR 0005. No mandatory architecture framework or new approval process is added.
