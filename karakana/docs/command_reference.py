"""Generate Karakana CLI command reference."""

from __future__ import annotations


COMMAND_GROUPS = {
    "version": ("Show package and runtime version metadata.", "karakana version", "Read-only.", "None", "karakana version"),
    "doctor": ("Run local health checks.", "karakana doctor", "Read-only plus local artifacts.", "None", "karakana doctor"),
    "config": ("Inspect and validate configuration.", "karakana config show\nkarakana config validate\nkarakana config paths", "Read-only.", "None", "karakana config validate"),
    "memory": ("Inspect ubongo memory.", "karakana memory validate --project karakana", "Read-only validation.", "None", "karakana memory validate --project karakana"),
    "skill": ("Inspect, validate, and index skills.", "karakana skill validate-all\nkarakana skill index", "Dry-run index by default.", "--write for index writes", "karakana skill validate-all"),
    "skillpack": ("Inspect and activate project skillpacks.", "karakana skillpack list\nkarakana skillpack activate karakana", "Activation writes local .karakana state only.", "None", "karakana skillpack validate-all"),
    "workspace": ("Coordinate read-only multi-project state.", "karakana workspace status\nkarakana workspace handoff --project nhrdm", "Read-only or artifact generation.", "None", "karakana workspace status"),
    "model": ("Inspect routing and controlled live model calls.", "karakana model route --task-type planning", "Dry-run unless --live is used.", "--live", "karakana model route --task-type planning"),
    "github": ("Generate GitHub artifacts and explicit writes.", "karakana github issue-draft", "Dry-run/artifact generation by default.", "Explicit create/comment flags", "karakana github --help"),
    "trace": ("Inspect local traces.", "karakana trace latest", "Read-only.", "None", "karakana trace latest"),
    "improve": ("Generate reviewable improvement proposals.", "karakana improve from-trace <run-id>", "Proposal only by default.", "--write or publish flags where supported", "karakana improve --help"),
    "action": ("Extract reviewable actions from model responses.", "karakana action extract --from-response <path>", "Artifact generation only.", "Publish flags are explicit", "karakana action list"),
    "codex": ("Generate Codex handoffs, capture diffs, review patches.", "karakana codex handoff <action-run-id>", "No Codex execution by default.", "--execute", "karakana codex capture-diff"),
    "patch": ("Gate, branch, apply, and commit reviewed patches locally.", "karakana patch gate --patch-run <id>", "Dry-run by default.", "--write, --create, --stage", "karakana patch status --patch-run <id>"),
    "ingest": ("Distill selected evidence into reviewable candidates.", "karakana ingest file README.md --classify", "No writes by default.", "--write", "karakana ingest list"),
    "requirements": ("Generate PRDs, stories, issues, and readiness checks.", "karakana requirements prd --from-note \"...\"", "Artifact generation only.", "--create-issues is explicit if supported", "karakana requirements list"),
    "crosslink": ("Detect reusable cross-project patterns.", "karakana crosslink scan --workspace nimr", "Scan/propose only; apply is dry-run.", "--write, --allow-high-risk", "karakana crosslink list"),
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
