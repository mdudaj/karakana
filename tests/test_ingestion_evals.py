from pathlib import Path

from karakana.evals.loader import EvalLoader


def test_ingestion_evals_discoverable():
    cases = EvalLoader(Path.cwd()).load_cases(suite="ingestion")

    assert {case.id for case in cases} >= {
        "ingestion-file-to-memory-candidate",
        "ingestion-redacts-secrets",
        "ingestion-skillpack-guides-targets",
    }
