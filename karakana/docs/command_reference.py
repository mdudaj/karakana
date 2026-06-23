"""Generate Karakana CLI command reference."""

from __future__ import annotations


COMMAND_GROUPS = {
    "version": ("Show package and runtime version metadata.", "karakana version", "Read-only.", "None", "karakana version"),
    "doctor": ("Run local health checks.", "karakana doctor", "Read-only plus local artifacts.", "None", "karakana doctor"),
    "config": ("Inspect and validate configuration.", "karakana config show\nkarakana config validate\nkarakana config paths", "Read-only.", "None", "karakana config validate"),
    "memory": ("Inspect ubongo memory.", "karakana memory validate --project karakana", "Read-only validation.", "None", "karakana memory validate --project karakana"),
    "handoff": ("Create and load project session handoffs.", "karakana handoff load --project msc-platform --skillpack msc-platform\nkarakana handoff refresh --project msc-platform --skillpack msc-platform", "Append-only local artifacts; load recovers bounded state when absent.", "--no-create, --no-write, --no-handoff", "karakana handoff doctor --project msc-platform"),
    "milestone": ("Decide the next project milestone and generate instructions.", "karakana milestone next --project msc-platform --skillpack msc-platform", "Artifact-only; strict mode blocks unresolved planning risk.", "--write-instructions", "Review .karakana/milestones/<run-id>/next-milestone.md"),
    "skill": ("Inspect, validate, and index skills.", "karakana skill validate-all\nkarakana skill index", "Dry-run index by default.", "--write for index writes", "karakana skill validate-all"),
    "skillpack": ("Inspect and activate project skillpacks.", "karakana skillpack list\nkarakana skillpack activate karakana", "Activation writes local .karakana state only.", "None", "karakana skillpack validate-all"),
    "workspace": ("Coordinate read-only multi-project state.", "karakana workspace status\nkarakana workspace handoff --project nhrdm", "Read-only or artifact generation.", "None", "karakana workspace status"),
    "model": ("Inspect routing and controlled live model calls.", "karakana model route --task-type planning", "Dry-run unless --live is used.", "--live", "karakana model route --task-type planning"),
    "github": ("Generate GitHub artifacts and explicit writes.", "karakana github issue-draft", "Dry-run/artifact generation by default.", "Explicit create/comment flags", "karakana github --help"),
    "trace": ("Inspect local traces.", "karakana trace latest", "Read-only.", "None", "karakana trace latest"),
    "improve": ("Generate reviewable improvement proposals.", "karakana improve from-trace <run-id>", "Proposal only by default.", "--write or publish flags where supported", "karakana improve --help"),
    "action": ("Extract reviewable actions from model responses.", "karakana action extract --from-response <path>", "Artifact generation only.", "Publish flags are explicit", "karakana action list"),
    "codex": ("Generate Codex handoffs, capture diffs, review patches, or start Codex with visible Karakana context.", "karakana codex start --project karakana --skillpack karakana -- --model gpt-5.5\nkarakana codex handoff <action-run-id>", "No Codex execution by default except explicit `codex start`; launcher prints and flushes handoff context before exec, injects session context as Codex's initial prompt for fresh interactive launches, and bootstraps a missing project .venv unless --no-bootstrap is used. If `karakana` is not on PATH and .venv is missing, use `python -m karakana codex start --project <project>` from the source checkout.", "--execute, --print-only, --no-create, --no-pause, --inline, --no-bootstrap, --no-inject-prompt", "karakana codex start --project karakana --skillpack karakana --print-only"),
    "copilot": ("Start GitHub Copilot CLI with visible Karakana handoff context.", "karakana copilot start --project karakana --skillpack karakana -- --model gpt-5.4", "Explicit launcher prints handoff context before exec; --print-only previews without launch.", "--print-only, --no-create, --no-pause", "karakana copilot start --project karakana --skillpack karakana --print-only"),
    "patch": ("Gate, branch, apply, and commit reviewed patches locally.", "karakana patch gate --patch-run <id>", "Dry-run by default.", "--write, --create, --stage", "karakana patch status --patch-run <id>"),
    "ingest": ("Distill selected evidence into reviewable candidates.", "karakana ingest file README.md --classify", "No writes by default.", "--write", "karakana ingest list"),
    "requirements": ("Generate PRDs, stories, issues, and readiness checks.", "karakana requirements prd --from-note \"...\"", "Artifact generation only.", "--create-issues is explicit if supported", "karakana requirements list"),
    "crosslink": ("Detect reusable cross-project patterns.", "karakana crosslink scan --workspace nimr", "Scan/propose only; apply is dry-run.", "--write, --allow-high-risk", "karakana crosslink list"),
    "protocol": ("Classify work, produce protocol artifacts, and gate reproducibility.", "karakana protocol start --task \"Plan a database schema migration\" --project karakana\nkarakana protocol template requirements_note\nkarakana protocol missing --trace <run-id>\nkarakana protocol attach --trace <run-id> --kind requirements_note --path docs/requirements/example.md\nkarakana protocol check --trace <run-id>", "Local artifact generation and trace updates only.", "--write-plan writes protocol-start artifacts; --output writes templates; handoff and patch gates use --require-protocol-pass for enforcement.", "karakana protocol validate-all"),
    "release": ("Run release checks and generate release artifacts.", "karakana release check\nkarakana release notes", "No publishing by default.", "--full runs slower local checks", "karakana release checklist"),
    "docs": ("Generate and check documentation.", "karakana docs command-reference\nkarakana docs check", "Preview by default.", "--write", "karakana docs check"),
}


def render_command_reference() -> str:
    lines = ["# Karakana Command Reference", ""]
    for group, (purpose, commands, safe_default, flags, example) in COMMAND_GROUPS.items():
        lines.extend(
            [
                f"## {group}",
                "",
                f"Purpose: {purpose}",
                "",
                "Common commands:",
                "```bash",
                commands,
                "```",
                "",
                f"Safe default behavior: {safe_default}",
                "",
                f"Write/execute flags: {flags}",
                "",
                "Example:",
                "```bash",
                example,
                "```",
                "",
            ]
        )
    return "\n".join(lines)
