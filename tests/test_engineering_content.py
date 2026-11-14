"""Real narrative checks, source-loss controls and explicit version and evidence limits."""

from pathlib import Path
import hashlib
import json
import shutil

import pytest

from karakana.tools.engineering_content import check_content, main


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def pack(tmp_path):
    for key, source in (
        ("req", "skills/engineering-requirements/assets/requirements-example.md"),
        ("design", "skills/engineering-design-records/assets/system-design-example.md"),
    ):
        shutil.copyfile(ROOT / source, tmp_path / f"{key}.md")
    context = {
        "context_version": "0.1", "namespace": "example",
        "documents": [
            {"key": "req", "path": "req.md", "format": "narrative-0.1",
             "profile": {"id": "requirements", "version": "0.1"}},
            {"key": "design", "path": "design.md", "format": "narrative-0.1",
             "profile": {"id": "system-design", "version": "0.1"}, "requirements": ["req"]},
        ],
    }
    (tmp_path / "context.json").write_text(json.dumps(context))
    return tmp_path, context


def run(pack):
    root, _ = pack
    return check_content(root, Path("context.json")).to_dict()


def mutate(pack, old, new, source="req.md"):
    path = pack[0] / source
    original = path.read_text()
    assert old in original
    path.write_text(original.replace(old, new))


def save_context(pack):
    (pack[0] / "context.json").write_text(json.dumps(pack[1]))


def test_real_packs_keep_identity_unknowns_and_sources(pack):
    before = {p: p.read_bytes() for p in pack[0].iterdir()}
    report = run(pack)
    assert report["completeness"] == "complete"
    assert report["review_required"] is True
    assert report["readiness"] == "unresolved"
    assert report["acceptance"] == "not_assessed"
    assert {d["document_id"] for d in report["documents"]} == {"EX-REQ", "EX-DES"}
    assert {item["record_id"] for item in report["open_acceptance_items"] if item["record_id"]} >= {"Q-01", "Q-02"}
    assert report["coverage"]["saved_report_verification"] == "supported"
    assert not any(f["severity"] == "error" for f in report["findings"])
    assert all(p.read_bytes() == value for p, value in before.items())


@pytest.mark.parametrize("feature", ["references", "coverage", "omissions", "open_items", "claims"])
def test_invalid_advanced_mappings_are_never_ignored(pack, feature):
    pack[1][feature] = [{}]
    save_context(pack)
    assert run(pack)["completeness"] == "incomplete"


def test_empty_advanced_arrays_are_accepted(pack):
    for feature in ("references", "coverage", "omissions", "open_items", "claims"):
        pack[1][feature] = []
    save_context(pack)
    assert run(pack)["completeness"] == "complete"


@pytest.mark.parametrize("fault", ["short", "wide", "leading", "trailing", "detached"])
def test_raw_table_candidates_cannot_be_padded_dropped_or_detached(pack, fault):
    path = pack[0] / "req.md"
    text = path.read_text()
    row = next(x for x in text.splitlines() if x.startswith("| REQ-01 |"))
    if fault == "short":
        bad = "| REQ-01 | Short row |"
    elif fault == "wide":
        bad = row + " discarded |"
    elif fault == "leading":
        bad = row[1:]
    elif fault == "trailing":
        bad = row[:-1]
    else:
        bad = row + "\n\nDetached prose\n" + row.replace("REQ-01", "REQ-99")
    path.write_text(text.replace(row, bad))
    assert run(pack)["completeness"] != "complete"


@pytest.mark.parametrize("fault", ["blank", "placeholder", "duplicate", "dangling", "one_way"])
def test_missing_requirement_content_and_reference_integrity(pack, fault):
    if fault == "blank":
        mutate(pack, "The portal shall permit record reading only when the reader has read permission and a current assignment to the record's programme.", " ")
    elif fault == "placeholder":
        mutate(pack, "The portal shall permit record reading", "{{requirement}} The portal shall permit record reading")
    elif fault == "duplicate":
        mutate(pack, "| REQ-02 |", "| REQ-01 |")
    elif fault == "dangling":
        mutate(pack, "| AC-01, AC-02 |", "| AC-99, AC-02 |")
    else:
        mutate(pack, "| AC-01, AC-02 |", "| AC-02 |")
    assert run(pack)["completeness"] == "incomplete"


def test_fenced_heading_does_not_supply_missing_context(pack):
    mutate(pack, "## Context and users", "```text\n## Context and users")
    mutate(pack, "## Functional requirements", "```\n## Functional requirements")
    assert run(pack)["completeness"] == "incomplete"


def test_wording_warns_without_banning_product_approval(pack):
    assert not any(f["rule_id"] == "CP-WORDING-001" for f in run(pack)["findings"])
    mutate(pack, "The portal shall permit record reading only when the reader has read permission and a current assignment to the record's programme.", "We will arrange a meeting to agree the requirements.")
    report = run(pack)
    assert report["completeness"] == "complete"
    assert any(f["rule_id"] == "CP-WORDING-001" and f["severity"] == "warning" for f in report["findings"])
    assert "We will arrange" not in json.dumps(report)


def test_crlf_semantics_equal_with_original_byte_freshness(pack):
    lf = run(pack)
    for name in ("req.md", "design.md"):
        path = pack[0] / name
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    crlf = run(pack)
    assert crlf["completeness"] == "complete"
    assert crlf["assessment_digest"] == lf["assessment_digest"]
    assert crlf["manifest"]["sources"] != lf["manifest"]["sources"]
    for source in crlf["manifest"]["sources"]:
        assert source["sha256"] == hashlib.sha256((pack[0] / source["path"]).read_bytes()).hexdigest()


def test_context_order_does_not_reallocate_or_change_assessment(pack):
    first = run(pack)
    pack[1]["documents"].reverse()
    save_context(pack)
    second = run(pack)
    assert first["assessment_digest"] == second["assessment_digest"]
    assert first["manifest"]["sources"] != second["manifest"]["sources"]


def test_cli_json_and_new_report_no_overwrite(pack, capsys):
    root = pack[0]
    args = ["--root", str(root), "check", "--context", "context.json", "--format", "json", "--output", "report.json"]
    assert main(args) == 0
    stdout = json.loads(capsys.readouterr().out)
    saved = json.loads((root / "report.json").read_text())
    assert stdout == saved and saved["completeness"] == "complete"
    before = (root / "report.json").read_bytes()
    assert main(args) == 2
    refusal = json.loads(capsys.readouterr().out)
    assert refusal["completeness"] != "complete"
    assert refusal['manifest']['sources'] == saved['manifest']['sources']
    assert (root / "report.json").read_bytes() == before


def test_verify_refuses_a_missing_saved_report(pack, capsys):
    assert main(["--root", str(pack[0]), "verify", "--context", "context.json", "--report", "old.json"]) == 2
    assert "stale, mismatched or incompatible" in capsys.readouterr().out


@pytest.mark.parametrize("text", [
    '{"context_version":"0.1","context_version":"0.1"}',
    '{"context_version":"0.1","namespace":"example","documents":NaN}',
    '{"context_version":"0.2","namespace":"example","documents":[]}',
])
def test_invalid_duplicate_non_json_or_unknown_version_never_pass(pack, text):
    (pack[0] / "context.json").write_text(text)
    assert run(pack)["completeness"] != "complete"


@pytest.mark.parametrize("path", ["../outside.md", ".env", "secrets/input.md", "private.key"])
def test_paths_refused_without_source_values(pack, path):
    pack[1]["documents"][0]["path"] = path
    save_context(pack)
    assert run(pack)["completeness"] != "complete"


@pytest.mark.parametrize("fault", ["unknown_key", "wrong_type", "duplicate_key", "duplicate_source", "missing_baseline", "wrong_profile", "p02", "links"])
def test_explicit_context_contract_and_baselines(pack, fault):
    context = pack[1]
    if fault == "unknown_key":
        context["documents"][0]["metadata_override"] = "secret-sentinel"
    elif fault == "wrong_type":
        context["documents"] = True
    elif fault == "duplicate_key":
        context["documents"][1]["key"] = "req"
    elif fault == "duplicate_source":
        context["documents"][1]["path"] = "req.md"
    elif fault == "missing_baseline":
        context["documents"][1].pop("requirements")
    elif fault == "wrong_profile":
        context["documents"][0]["profile"]["id"] = "../../unsafe"
    elif fault == "p02":
        context["documents"][0]["format"] = "p02-0.1"
    else:
        context["links"] = []
    save_context(pack)
    report = run(pack)
    assert report["completeness"] != "complete"
    assert "secret-sentinel" not in json.dumps(report)


@pytest.mark.parametrize("fault", ["header", "separator", "duplicate_heading", "duplicate_anchor", "bom", "standalone_cr", "control", "claim_table"])
def test_unconsumed_declarations_and_unsupported_shapes(pack, fault):
    if fault == "header":
        mutate(pack, "| ID | Requirement |", "| ID | Changed Header |")
    elif fault == "separator":
        mutate(pack, "| --- | --- | --- | --- |", "| --- | --- | --- |")
    elif fault == "duplicate_heading":
        mutate(pack, "## Functional requirements", "## Functional requirements\n\n## 04 Functional requirements")
    elif fault == "duplicate_anchor":
        mutate(pack, "## Functional requirements", '<a id="same"></a>\n## Functional requirements\n\n<a id="same"></a>')
    elif fault == "bom":
        p = pack[0] / "req.md"
        p.write_bytes(b'\xef\xbb\xbf' + p.read_bytes())
    elif fault == "standalone_cr":
        p = pack[0] / "req.md"
        p.write_bytes(p.read_bytes().replace(b'\n', b'\r'))
    elif fault == "control":
        mutate(pack, "# Programme", "# \x1bProgramme")
    else:
        with (pack[0] / "req.md").open("a") as stream:
            stream.write('\n## Observed results\n\n| Test | Result |\n| --- | --- |\n| T-01 | Pass |\n')
    result = run(pack)
    assert result["completeness"] != "complete"
    assert {d['key'] for d in result['documents']} == {'req', 'design'}
    assert next(d for d in result['documents'] if d['key'] == 'req')['completeness'] != 'complete'


def test_literal_syntax_encoded_cells_and_formula_looking_text_are_not_executed(pack):
    mutate(pack, "The portal shall permit record reading", "The portal shall render `{{literal}}`, &#124; and =SUM(1,2) before permitting record reading")
    assert run(pack)["completeness"] == "complete"


def test_empty_requirement_rows_are_not_completed_content(pack):
    p = pack[0] / "req.md"
    text = p.read_text()
    rows = [x for x in text.splitlines() if x.startswith("| REQ-")]
    for row in rows:
        text = text.replace(row, "|  |  |  |  |")
    p.write_text(text)
    assert run(pack)["completeness"] == "incomplete"


def test_no_fixed_global_record_count_and_no_invented_open_items(pack):
    # A legitimately absent optional unresolved section does not mean ready.
    p = pack[0] / "req.md"
    p.write_text(p.read_text().split('## Unresolved matters')[0])
    # Other source references still require Q-01, so don't pretend they're resolved.
    report = run(pack)
    assert report["completeness"] != "complete"
    assert report["acceptance"] == "not_assessed"
    assert report["review_required"] is True


def test_missing_reference_range_member_is_not_silently_expanded(pack):
    mutate(pack, "AC-01–AC-03 integration matrix", "AC-01–AC-999999999999 integration matrix", "design.md")
    assert run(pack)["completeness"] == "incomplete"


def test_unmapped_accepted_decision_does_not_get_approval(pack):
    mutate(pack, "; Proposed |", "; Accepted |", "design.md")
    report = run(pack)
    assert report["completeness"] == "incomplete"
    assert report["acceptance"] == "not_assessed"


def test_source_change_during_read_refuses_current_run(pack, monkeypatch):
    from karakana.tools import engineering_content as tool
    original = tool.read_narrative
    def changed(raw, key, path, profile, md, mapped_slots=()):
        result = original(raw, key, path, profile, md, mapped_slots)
        if key == "req":
            with (pack[0] / path).open("a") as stream:
                stream.write('\nChanged during read.\n')
        return result
    monkeypatch.setattr(tool, 'read_narrative', changed)
    report = run(pack)
    assert report["completeness"] == "incomplete"
    assert any(f['rule_id'] == 'CP-DRIFT-001' for f in report['findings'])


def test_change_after_check_prevents_report_output(pack, monkeypatch, capsys):
    from karakana.tools import engineering_content as tool
    original = tool.check_content
    def changed(*args):
        result = original(*args)
        with (pack[0] / 'req.md').open('a') as stream:
            stream.write('\nAfter assessment.\n')
        return result
    monkeypatch.setattr(tool, 'check_content', changed)
    assert main(['--root', str(pack[0]), 'check', '--context', 'context.json', '--output', 'fresh.json', '--format', 'json']) == 2
    assert not (pack[0] / 'fresh.json').exists()
    assert any(f['rule_id'] == 'CP-DRIFT-001' for f in json.loads(capsys.readouterr().out)['findings'])


def test_checker_source_change_during_assessment_is_detected(pack, monkeypatch, tmp_path):
    from karakana.content_profiles import report as reporting
    from karakana.tools import engineering_content as tool
    code = tmp_path / 'code'
    shutil.copytree(ROOT / 'karakana/content_profiles', code)
    original_files = reporting.files
    monkeypatch.setattr(reporting, 'files', lambda name: code if name == 'karakana.content_profiles' else original_files(name))
    original = tool.read_narrative
    def changed(*args):
        result = original(*args)
        if args[1] == 'req':
            with (code / 'checks.py').open('a') as stream:
                stream.write('\n# changed after reading started\n')
        return result
    monkeypatch.setattr(tool, 'read_narrative', changed)
    result = run(pack)
    assert result['completeness'] == 'incomplete'
    assert any(f['rule_id'] == 'CP-DRIFT-001' for f in result['findings'])


def test_profile_bytes_change_during_assessment_is_detected(pack, monkeypatch, tmp_path):
    from karakana.content_profiles import loader
    from karakana.tools import engineering_content as tool
    resources = tmp_path / 'profiles'
    shutil.copytree(ROOT / 'karakana/content_profiles', resources)
    monkeypatch.setattr(loader, 'files', lambda name: resources)
    original = tool.read_narrative
    def changed(*args):
        result = original(*args)
        if args[1] == 'req':
            with (resources / 'requirements-0.1.json').open('a') as stream:
                stream.write('\n')
        return result
    monkeypatch.setattr(tool, 'read_narrative', changed)
    assert any(f['rule_id'] == 'CP-DRIFT-001' for f in run(pack)['findings'])


def test_symlink_escape_is_refused_before_read(pack, tmp_path):
    outside = tmp_path.parent / (tmp_path.name + '-outside.md')
    outside.write_text('private-sentinel')
    target = pack[0] / 'link.md'
    target.symlink_to(outside)
    pack[1]['documents'][0]['path'] = 'link.md'
    save_context(pack)
    report = run(pack)
    assert report['completeness'] != 'complete'
    assert 'private-sentinel' not in json.dumps(report)


def test_document_and_context_byte_limits(pack):
    p = pack[0] / 'req.md'
    p.write_bytes(b'x' * 2_000_001)
    assert any(f['rule_id'] == 'CP-LIMIT-001' for f in run(pack)['findings'])
    (pack[0] / 'context.json').write_bytes(b' ' * 128_001)
    assert any(f['rule_id'] == 'CP-LIMIT-001' for f in run(pack)['findings'])


def test_aggregate_limit(pack, monkeypatch):
    from karakana.content_profiles import loader
    monkeypatch.setattr(loader, 'MAX_TOTAL_BYTES', 1000)
    assert any(f['rule_id'] == 'CP-LIMIT-001' for f in run(pack)['findings'])


def test_file_count_limit_includes_context(pack):
    context = pack[1]
    context['documents'] = []
    for i in range(32):
        shutil.copyfile(pack[0] / 'req.md', pack[0] / f'req{i}.md')
        context['documents'].append({'key': f'r{i}', 'path': f'req{i}.md', 'format': 'narrative-0.1', 'profile': {'id': 'requirements', 'version': '0.1'}})
    save_context(pack)
    assert any(f['rule_id'] == 'CP-LIMIT-001' for f in run(pack)['findings'])


def test_report_does_not_dump_statements_or_extra_metadata(pack):
    mutate(pack, '| Document ID | EX-REQ |', '| Private configuration | private-sentinel |\n| Document ID | EX-REQ |')
    report = run(pack)
    assert report['completeness'] == 'complete'
    assert 'private-sentinel' not in json.dumps(report)
    assert "The portal shall" not in json.dumps(report)


def test_proposed_decision_about_accepted_product_state_is_not_an_approval_claim(pack):
    mutate(pack, 'ADR-01: shared server-side policy', 'ADR-01: Accepted record states use shared server-side policy', 'design.md')
    assert run(pack)['completeness'] == 'complete'


def test_missing_root_and_symlink_loop_have_controlled_cli_errors(pack, capsys):
    root = pack[0] / 'absent'
    assert main(['--root', str(root), 'check', '--context', 'context.json', '--format', 'json']) == 2
    assert json.loads(capsys.readouterr().out)['completeness'] == 'incomplete'
    link = pack[0] / 'loop'
    link.symlink_to(link)
    assert main(['--root', str(link), 'check', '--context', 'context.json', '--format', 'json', '--output', 'out.json']) == 2
    assert json.loads(capsys.readouterr().out)['completeness'] == 'incomplete'


def test_retargeted_source_symlink_with_equal_bytes_is_stale_before_output(pack, monkeypatch, capsys):
    from karakana.tools import engineering_content as tool
    root = pack[0]
    shutil.copyfile(root / 'req.md', root / 'same.md')
    link = root / 'selected.md'
    link.symlink_to('req.md')
    pack[1]['documents'][0]['path'] = 'selected.md'
    save_context(pack)
    original = tool.check_content
    def changed(*args):
        result = original(*args)
        link.unlink(); link.symlink_to('same.md')
        return result
    monkeypatch.setattr(tool, 'check_content', changed)
    assert main(['--root', str(root), 'check', '--context', 'context.json', '--format', 'json', '--output', 'out.json']) == 2
    assert not (root / 'out.json').exists()
    assert any(f['rule_id'] == 'CP-DRIFT-001' for f in json.loads(capsys.readouterr().out)['findings'])


def test_extreme_json_integer_has_a_controlled_refusal(pack):
    (pack[0] / 'context.json').write_text('{"context_version":' + '9' * 6000 + '}')
    assert run(pack)['completeness'] != 'complete'


@pytest.mark.parametrize('fault', ['record_kind', 'non_string_check'])
def test_invalid_packaged_rule_data_refuses_instead_of_skipping_checks(pack, monkeypatch, tmp_path, fault):
    from karakana.content_profiles import loader
    resources = tmp_path / 'resources'
    shutil.copytree(ROOT / 'karakana/content_profiles', resources)
    p = resources / 'requirements-0.1.json'
    data = json.loads(p.read_text())
    if fault == 'record_kind':
        data['tables'][2]['record_type'] = 'skip_record_validation'
    else:
        data['checks'][0] = {}
    p.write_text(json.dumps(data))
    monkeypatch.setattr(loader, 'files', lambda name: resources)
    assert run(pack)['completeness'] != 'complete'
