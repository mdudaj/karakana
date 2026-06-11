from karakana.ingestion.scanner import scan_sources


def test_scan_conservative_defaults(tmp_path):
    (tmp_path / "README.md").write_text("architecture decision\n", encoding="utf-8")
    (tmp_path / "karakana").mkdir()
    (tmp_path / "karakana" / "source.py").write_text("do not scan\n", encoding="utf-8")

    sources = scan_sources(tmp_path, project="karakana")

    assert len(sources) == 1
    assert sources[0][0].path == "README.md"


def test_msc_platform_scan_prefers_stemgen_docs(tmp_path):
    karakana_root = tmp_path / "karakana"
    karakana_root.mkdir()
    (karakana_root / "README.md").write_text("generic karakana docs\n", encoding="utf-8")
    platform_root = tmp_path / "stemgen-platform"
    (platform_root / "docs" / "research").mkdir(parents=True)
    (platform_root / "docs" / "research" / "objective-feature-evidence-matrix.md").write_text("research objective evidence artifact\n", encoding="utf-8")

    sources = scan_sources(karakana_root, project="msc-platform", skillpack="msc-platform")

    assert sources
    assert sources[0][0].path == "docs/research/objective-feature-evidence-matrix.md"
