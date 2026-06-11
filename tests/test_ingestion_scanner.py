from karakana.ingestion.scanner import scan_sources


def test_scan_conservative_defaults(tmp_path):
    (tmp_path / "README.md").write_text("architecture decision\n", encoding="utf-8")
    (tmp_path / "karakana").mkdir()
    (tmp_path / "karakana" / "source.py").write_text("do not scan\n", encoding="utf-8")

    sources = scan_sources(tmp_path, project="karakana")

    assert len(sources) == 1
    assert sources[0][0].path == "README.md"
