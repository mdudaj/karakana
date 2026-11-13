# Documentation and parser integrity: continuation

The accepted requirements/design directions and CT01–CT08 convention/template
slice are integrated through PR #36 at `f2319cc`. Preserve that completed work.
The [parent plan](DRAFTING-CONVENTIONS-2026-11-13.md) retains decisions and the
remaining roadmap.

The next PI01–PI08 parser slice has a complete
[research, implementation and verification record](PARSER-INTEGRITY-2026-11-13.md).
Its local checkpoint passed 140 focused tests, 818 full tests and 183 deterministic
evals. It fixes LF/CRLF record loss and silent malformed-row filtering, preserving
raw-byte hashes, valid empty tables, narrative sources and native/source authority.
No mandatory content profile, general Markdown engine or automatic selection/
enforcement was added. The clean narrative assets remain outside P02's structured
source contract.

First inspect current `main`, the PI code/tests and the associated PR state.
The owner selected source review/publication/squash integration after local
verification. If integration is pending, finish that task on
`research/engineering-artifact-parser-integrity-20261113` under its recorded
authority and exact-head checks. If it is merged, carry the receipt forward and
select the next bounded roadmap task instead of reopening research or the fix.

After integration, the next candidate is bounded content-profile/checks resolution:
which document-specific completeness checks should supplement structural parsing
without rejecting legitimate narrative/empty states or inventing substantive
approval. Reuse the accepted conventions and prior findings; settle scope, method,
compatibility and tests before its own implementation. Task-time resource selection/
enforcement, remaining template/export packs, pilot and Jovina retain later scope.

Follow repository instructions, load the current task handoff and use a task
branch for edits. Verify evidence before claiming integration or acceptance; the
linked records retain historical checkpoints. No app-server connection, live
model calls or client revisions are needed. Loading is context, not fresh external
publication, merge or deployment authority.
