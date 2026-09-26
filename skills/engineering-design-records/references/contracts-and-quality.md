# Interfaces, quality and UX in design records

For each affected interface identify authority/path/version, input/output schema,
state/error semantics, invariants and compatibility. Link executable contracts and
examples in their owning source. A Markdown summary does not override machine schema
or existing access-control/process rules. Resolve divergence explicitly.

Describe relevant data/security/operations concerns: data lifecycle/retention, trust
boundaries, authorized actors, failure modes, recovery and observability. Record risk
assumptions and the actual verification method/evidence needed. Sensitive production
values stay out of shared artifacts. A security checklist is not threat validation.

A quality requirement needs scoped workload/environment/measure/threshold and how to
observe it. Keep thresholds unconfirmed when unresolved; project agreement is needed
before an invented target becomes an acceptance condition.

When UX is affected, describe behavior and look/feel before implementation: states,
copy, navigation, errors/empty states, keyboard/assistive interaction and existing
shared components/tokens. Load the relevant domain/UX/design-system skill for the
actual stack. Document reusable system patterns rather than page-local styling.

Assess migrations and compatibility at the document level without executing them.
Separate proposed design, executable source and actual observation. Use UX and
Contracts/Design Views/Risks only where applicable. Basis:
[research/plan](../../../docs/skills/engineering-artifact-catalogue/PLAN.md), S06/S20–S22,
and the existing engineering lifecycle; drafting never grants operational authority.
