"""Project-specific requirement slices for stemgen-platform."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MscPlatformSlice:
    suffix: str
    title: str
    research_objective: str
    research_question: str
    platform_capability: str
    workflow: str
    evidence_artifact: str
    schema_artifact: str
    target_files: tuple[str, ...]
    out_of_scope: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]
    verification_command: str
    safety_constraints: tuple[str, ...]
    definition_of_done: tuple[str, ...]
    risk_level: str = "medium"


MSC_PLATFORM_SLICES: tuple[MscPlatformSlice, ...] = (
    MscPlatformSlice(
        suffix="slice-1a",
        title="Slice 1A: Curriculum source registry schema",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Which official curriculum sources provide authoritative topic facts?",
        platform_capability="Tiered curriculum source registry.",
        workflow="curriculum intake",
        evidence_artifact="source_registry.json",
        schema_artifact="schemas/curriculum/source_registry.schema.json",
        target_files=("schemas/curriculum/source_registry.schema.json", "docs/schemas/README.md"),
        out_of_scope=("live TIE downloads", "curriculum extraction", "topic screening"),
        acceptance_criteria=(
            "Schema requires source_id, title, official_url, publisher, source_tier, expected local snapshot path, and checksum requirement.",
            "Schema examples cover the four required TIE sources.",
            "Validation fails if Tier 2-4 sources are allowed to override Tier 1 facts.",
        ),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("Do not read .env files.", "Do not fetch live sources in this slice."),
        definition_of_done=("Schema validates.", "Example fixture validates.", "Documentation links schema to curriculum source registry evidence."),
    ),
    MscPlatformSlice(
        suffix="slice-1b",
        title="Slice 1B: TIE source registry fixture",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Are the official TIE sources registered reproducibly?",
        platform_capability="Versioned source registry fixture.",
        workflow="curriculum intake",
        evidence_artifact="source_registry.json",
        schema_artifact="schemas/curriculum/source_registry.schema.json",
        target_files=("fixtures/examples/source_registry.example.json",),
        out_of_scope=("live source download", "checksum generation from remote files", "manual topic acceptance"),
        acceptance_criteria=(
            "Fixture includes Primary Education Curriculum, Science, Mathematics, and Geography TIE URLs.",
            "Each fixture item records Tier 1 source status and expected local snapshot path.",
            "Fixture validates against the source registry schema.",
        ),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("Use official public URLs only.", "Do not include downloaded copyrighted PDF content in Git."),
        definition_of_done=("All four TIE entries are present.", "Fixture validates offline.", "No secrets or participant data are present."),
    ),
    MscPlatformSlice(
        suffix="slice-1c",
        title="Slice 1C: Curriculum source snapshot manifest schema",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can a curriculum source snapshot be reconstructed and audited?",
        platform_capability="Snapshot manifest contract.",
        workflow="curriculum intake",
        evidence_artifact="curriculum_snapshot_manifest.json",
        schema_artifact="schemas/curriculum/curriculum_snapshot_manifest.schema.json",
        target_files=("schemas/curriculum/curriculum_snapshot_manifest.schema.json", "fixtures/examples/curriculum_snapshot_manifest.example.json"),
        out_of_scope=("actual PDF download", "OCR/text extraction", "candidate topic generation"),
        acceptance_criteria=(
            "Schema records snapshot_id, created_at, source registry reference, downloaded source entries, checksums, and retrieval method.",
            "Example manifest references the four TIE source IDs without embedding source document contents.",
            "Manifest validates offline.",
        ),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("Do not store source document contents in the manifest.", "Do not require network access."),
        definition_of_done=("Schema validates.", "Example validates.", "Manifest fields are sufficient for later replay/audit."),
    ),
    MscPlatformSlice(
        suffix="slice-1d",
        title="Slice 1D: Local downloaded-source archive layout",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Where are official source snapshots stored for reproducibility?",
        platform_capability="Local archive layout convention.",
        workflow="curriculum intake",
        evidence_artifact="downloaded_sources/",
        schema_artifact="schemas/curriculum/curriculum_snapshot_manifest.schema.json",
        target_files=("docs/schemas/README.md", "docs/curriculum/tie-source-snapshot-plan.md"),
        out_of_scope=("committing large binary PDFs", "live downloads", "data extraction"),
        acceptance_criteria=(
            "Archive layout is documented under artifacts/curriculum-snapshots/<snapshot_id>/downloaded_sources/.",
            "The layout separates registry, manifests, downloaded files, checksums, and extracted data.",
            "Docs warn against committing copyrighted source binaries unless explicitly approved.",
        ),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("Do not commit generated datasets by default.", "Do not commit copyrighted PDFs by default."),
        definition_of_done=("Layout is documented.", "Snapshot manifest example reflects the layout.", "Validation command remains offline."),
    ),
    MscPlatformSlice(
        suffix="slice-1e",
        title="Slice 1E: SHA-256 checksum manifest",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can source snapshots be verified against recorded hashes?",
        platform_capability="Checksum manifest contract.",
        workflow="curriculum intake",
        evidence_artifact="checksums.sha256",
        schema_artifact="schemas/curriculum/fetch_manifest.schema.json",
        target_files=("schemas/curriculum/fetch_manifest.schema.json", "scripts/validate_json.py"),
        out_of_scope=("remote checksum verification", "live fetch retries", "PDF parsing"),
        acceptance_criteria=(
            "Fetch manifest schema records source_id, URL, local path, retrieval status, and SHA-256 checksum.",
            "Validation guidance explains checksum manifest expectations.",
            "Example data validates without network access.",
        ),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("Do not fetch remote files in validation.", "Do not log credentials."),
        definition_of_done=("Fetch manifest schema validates.", "Checksum fields are required.", "Offline validation passes."),
    ),
    MscPlatformSlice(
        suffix="slice-1f",
        title="Slice 1F: Snapshot validation command",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can operators validate source registry and snapshot evidence before extraction?",
        platform_capability="Offline schema validation command.",
        workflow="curriculum intake",
        evidence_artifact="validation report for source registry and snapshot manifests",
        schema_artifact="scripts/validate_json.py",
        target_files=("scripts/validate_json.py",),
        out_of_scope=("live model calls", "live WhatsApp messaging", "live TIE downloads"),
        acceptance_criteria=(
            "Command validates JSON syntax for tracked JSON files.",
            "Command validates known example fixtures against schemas.",
            "Command fails clearly on invalid JSON or schema validation errors.",
        ),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("Validation must not require network access.", "Validation must not read .env or secrets."),
        definition_of_done=("Validation passes on examples.", "Failure messages include file and schema paths.", "Command is documented in VERIFICATION.md."),
    ),
    MscPlatformSlice(
        suffix="slice-1g",
        title="Slice 1G: Snapshot docs and tests",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Is Slice 1 ready for implementation without ambiguity?",
        platform_capability="Schema-backed snapshot documentation and verification.",
        workflow="curriculum intake",
        evidence_artifact="source registry, fetch manifest, snapshot manifest, checksum manifest",
        schema_artifact="docs/schemas/README.md",
        target_files=("docs/schemas/README.md", "VERIFICATION.md"),
        out_of_scope=("deterministic extraction", "topic screening", "human topic selection"),
        acceptance_criteria=(
            "Docs identify Slice 1 required schemas.",
            "Verification docs include ./init.sh and python3 scripts/validate_json.py.",
            "Docs explain that schema changes are research-contract changes.",
        ),
        verification_command="./init.sh && python3 scripts/validate_json.py",
        safety_constraints=("No live TIE fetch is required.", "No generated evaluation data is committed."),
        definition_of_done=("Docs are updated.", "Examples validate.", "Slice 1 acceptance criteria are explicit."),
    ),
    MscPlatformSlice(
        suffix="slice-2a",
        title="Slice 2A: Normalized curriculum item schema",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can extracted curriculum facts be represented without LLM overwrite?",
        platform_capability="Deterministic curriculum extraction contract.",
        workflow="deterministic curriculum extraction",
        evidence_artifact="normalized_curriculum_items.json",
        schema_artifact="schemas/curriculum/curriculum_item.schema.json",
        target_files=("schemas/curriculum/curriculum_item.schema.json", "fixtures/examples/curriculum_item.example.json"),
        out_of_scope=("OCR implementation", "LLM enrichment", "topic promotion"),
        acceptance_criteria=("Schema captures source references, subject, standard, topic, subtopic, learning objective, content reference, and provenance.",),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("LLM output must not overwrite deterministic fields.",),
        definition_of_done=("Schema and example validate.",),
    ),
    MscPlatformSlice(
        suffix="slice-3a",
        title="Slice 3A: Rule-based topic screening schema",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can animation suitability be screened deterministically before review?",
        platform_capability="Candidate topic dataset contract.",
        workflow="topic screening",
        evidence_artifact="candidate_topic_dataset.json",
        schema_artifact="schemas/curriculum/candidate_topic_dataset.schema.json",
        target_files=("schemas/curriculum/candidate_topic_dataset.schema.json",),
        out_of_scope=("LLM review", "human acceptance", "generation run"),
        acceptance_criteria=("Schema records suitability signals, deprioritization reasons, source item IDs, and review status.",),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("Screening cannot auto-accept topics.",),
        definition_of_done=("Schema validates.",),
    ),
    MscPlatformSlice(
        suffix="slice-4a",
        title="Slice 4A: Automated curriculum review distribution schema",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can optional automated review expose uncertainty before human selection?",
        platform_capability="Verbalized-sampling-inspired review artifact.",
        workflow="automated curriculum review",
        evidence_artifact="candidate_topic_review_distribution.json",
        schema_artifact="schemas/curriculum/candidate_topic_review_distribution.schema.json",
        target_files=("schemas/curriculum/candidate_topic_review_distribution.schema.json", "fixtures/examples/candidate_topic_review_distribution.example.json"),
        out_of_scope=("live LLM calls", "topic auto-selection", "curriculum fact mutation"),
        acceptance_criteria=("Schema requires judgment distributions, rationales, uncertainty flags, input hashes, and human_review_required=true.",),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("LLM review is optional and assistive only.", "Human review remains required."),
        definition_of_done=("Schema and example validate.",),
        risk_level="high",
    ),
    MscPlatformSlice(
        suffix="slice-5a",
        title="Slice 5A: Human topic selection decision schema",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can accepted topics be traced to human review decisions?",
        platform_capability="Human topic selection gate.",
        workflow="human topic selection",
        evidence_artifact="topic_selection_decisions.json",
        schema_artifact="schemas/curriculum/topic_selection_decisions.schema.json",
        target_files=("schemas/curriculum/topic_selection_decisions.schema.json", "fixtures/examples/topic_selection_decisions.example.json"),
        out_of_scope=("automated acceptance", "generation runs", "classroom deployment"),
        acceptance_criteria=("Schema records reviewer, decision, reviewed_at, source checks, automated review considered, and rationale.",),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("No topic promotion without human acceptance.",),
        definition_of_done=("Schema and example validate.",),
    ),
    MscPlatformSlice(
        suffix="slice-8a",
        title="Slice 8A: Expert review submission schema",
        research_objective="Evaluate feasibility in terms of curriculum alignment, scientific accuracy, pedagogical appropriateness, clarity, usability, and production practicality.",
        research_question="Can expert evaluations be captured as analysis-ready evidence?",
        platform_capability="Rubric response contract.",
        workflow="expert review submission",
        evidence_artifact="rubric_response.json",
        schema_artifact="schemas/evaluation/rubric_response.schema.json",
        target_files=("schemas/evaluation/rubric.schema.json", "schemas/evaluation/rubric_response.schema.json"),
        out_of_scope=("participant-sensitive classroom data", "WhatsApp-only review", "statistical effectiveness claims"),
        acceptance_criteria=("Schema links evaluator, invitation, artifact set, scores, comments, and submitted_at.",),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("Do not store participant-sensitive data in fixtures.",),
        definition_of_done=("Rubric and response schemas validate.",),
    ),
    MscPlatformSlice(
        suffix="slice-9a",
        title="Slice 9A: Evidence export manifest schema",
        research_objective="Evaluate feasibility in terms of curriculum alignment, scientific accuracy, pedagogical appropriateness, clarity, usability, and production practicality.",
        research_question="Can evidence bundles be exported for descriptive analysis?",
        platform_capability="Evidence export contract.",
        workflow="export for descriptive analysis",
        evidence_artifact="export_manifest.json",
        schema_artifact="schemas/evaluation/export_manifest.schema.json",
        target_files=("schemas/evaluation/export_manifest.schema.json",),
        out_of_scope=("publication upload", "PR creation", "live dashboard analytics"),
        acceptance_criteria=("Schema records export batch, included files, formats, hashes, and privacy notes.",),
        verification_command="python3 scripts/validate_json.py",
        safety_constraints=("Exports must not include secrets or unredacted sensitive data.",),
        definition_of_done=("Schema validates.",),
    ),
)


MSC_PLATFORM_CURRICULUM_INTAKE_UX_SLICES: tuple[MscPlatformSlice, ...] = (
    MscPlatformSlice(
        suffix="slice-1-1a",
        title="Slice 1.1A: Staff curriculum intake management surface",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can staff operators prepare official TIE source evidence before extraction?",
        platform_capability="Staff-only curriculum intake management UX.",
        workflow="curriculum intake management",
        evidence_artifact="source registry and snapshot status handoff",
        schema_artifact="schemas/curriculum/source_registry.schema.json",
        target_files=("apps/curriculum/views.py", "apps/curriculum/urls.py", "templates/curriculum/", "templates/app/page.html"),
        out_of_scope=("curriculum extraction", "topic screening", "automated curriculum review", "human topic selection"),
        acceptance_criteria=(
            "Staff users can reach a curriculum intake management page from dashboard or curriculum navigation.",
            "The page shows active source count, Tier 1 count, latest snapshot status, validation status, warning count, and artifact paths when present.",
            "Anonymous and non-staff users cannot access intake management actions.",
        ),
        verification_command="python manage.py test apps.curriculum",
        safety_constraints=("Keep intake actions staff-only.", "Do not expose secrets or source document contents."),
        definition_of_done=("Staff-only access is tested.", "Dashboard/navigation link is tested.", "Existing read-only snapshot pages still pass."),
    ),
    MscPlatformSlice(
        suffix="slice-1-1b",
        title="Slice 1.1B: Seed default TIE source action",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Are the default official TIE sources registered reproducibly?",
        platform_capability="Idempotent default TIE source seeding.",
        workflow="curriculum intake management",
        evidence_artifact="source_registry.json",
        schema_artifact="schemas/curriculum/source_registry.schema.json",
        target_files=("apps/curriculum/services.py", "apps/curriculum/views.py", "fixtures/curriculum/tie_sources.json"),
        out_of_scope=("live TIE downloads", "fixture schema redesign", "topic acceptance"),
        acceptance_criteria=(
            "Staff users can seed default Tier 1 TIE sources through a POST action.",
            "The action reuses seed_curriculum_sources and is idempotent by source_id.",
            "The UI reports created or updated source count without creating duplicate rows.",
        ),
        verification_command="python manage.py test apps.curriculum",
        safety_constraints=("Use the existing fixture as the source of default TIE entries.", "Do not commit downloaded PDFs."),
        definition_of_done=("Seed action is tested through the view.", "Repeated seed action does not duplicate sources.", "Dashboard source count reflects seeded active sources."),
    ),
    MscPlatformSlice(
        suffix="slice-1-1c",
        title="Slice 1.1C: Add or update TIE source action",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can missing official TIE links be registered with enough metadata for reproducible snapshots?",
        platform_capability="Validated TIE source registration form.",
        workflow="curriculum intake management",
        evidence_artifact="source_registry.json",
        schema_artifact="schemas/curriculum/source_registry.schema.json",
        target_files=("apps/curriculum/models.py", "apps/curriculum/views.py", "templates/curriculum/"),
        out_of_scope=("source approval workflow", "non-TIE source tiers unless explicitly approved", "curriculum extraction"),
        acceptance_criteria=(
            "Staff users can add or deliberately update a TIE source with source_id, title, official URL, subject, coverage, standards, expected filename, tier, and active flag.",
            "Validation rejects invalid source IDs, invalid URLs, missing metadata, unsafe filenames, and unintended duplicate source IDs.",
            "Tier 1 source actions are limited to official TIE URLs unless a later approved requirement expands source tiers.",
        ),
        verification_command="python manage.py test apps.curriculum",
        safety_constraints=("Curriculum source changes remain approval-gated.", "Do not allow user input to create unsafe filenames or paths."),
        definition_of_done=("Valid add-source flow is tested.", "Validation failures are tested.", "Duplicate-source behavior is explicit and tested."),
    ),
    MscPlatformSlice(
        suffix="slice-1-1d",
        title="Slice 1.1D: Capture snapshot action",
        research_objective="Identify Tanzanian primary STEM curriculum topics suitable for animation-based representation.",
        research_question="Can staff operators capture or rehearse official source snapshots while preserving audit evidence?",
        platform_capability="Explicit-mode source snapshot capture.",
        workflow="curriculum intake management",
        evidence_artifact="fetch_manifest.json, checksums.sha256, curriculum_snapshot_manifest.json",
        schema_artifact="schemas/curriculum/curriculum_snapshot_manifest.schema.json",
        target_files=("apps/curriculum/services.py", "apps/curriculum/views.py", "templates/curriculum/"),
        out_of_scope=("network-dependent tests", "PDF parsing", "candidate topic generation"),
        acceptance_criteria=(
            "Staff users can capture a snapshot through existing create_snapshot service behavior.",
            "The action exposes explicit snapshot_id, validate, no-download, local-cache reuse, and live retrieval choices.",
            "Duplicate snapshot IDs or existing artifact directories are shown as action errors rather than server errors.",
            "Tests use no-download, local-cache, or injected fetch behavior and do not require live network access.",
        ),
        verification_command="python manage.py test apps.curriculum",
        safety_constraints=("Live retrieval must be an explicit staff action.", "Do not commit generated local snapshot artifacts."),
        definition_of_done=("No-download or local-cache capture is tested through the view.", "Duplicate snapshot failure is tested.", "Warnings and validation errors are visible in the UI."),
    ),
)


def is_msc_platform(project: str | None) -> bool:
    return project == "msc-platform"


def slices_for_prd(project: str | None, title: str, goal: str, context: str) -> tuple[MscPlatformSlice, ...]:
    if not is_msc_platform(project):
        return ()
    text = f"{title}\n{goal}\n{context}".lower()
    if "slice 1.1" in text or "curriculum intake management ux" in text or "tie source actions" in text:
        return MSC_PLATFORM_CURRICULUM_INTAKE_UX_SLICES
    return MSC_PLATFORM_SLICES
