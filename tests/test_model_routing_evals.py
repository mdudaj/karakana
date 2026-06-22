from pathlib import Path

from karakana.evals.loader import EvalLoader


def test_model_routing_evals_are_discoverable():
    ids = {case.id for case in EvalLoader(Path.cwd()).load_cases(suite="model-routing")}

    assert "model-routing-haiku-for-documentation" in ids
    assert "model-routing-codex-mini-for-routine-code" in ids
    assert "model-routing-codex-5-5-for-payment-logic" in ids
