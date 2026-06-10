import pytest

from karakana.patch.schemas import PatchApplyResult, PatchBranchPlan, PatchCommitResult, PatchGateResult


def test_patch_gate_schema():
    result = PatchGateResult("patch", "passed", "low", False)
    assert result.to_dict()["patch_run_id"] == "patch"


def test_patch_schema_validation():
    with pytest.raises(ValueError):
        PatchApplyResult("patch", "bad", True, False)
    with pytest.raises(ValueError):
        PatchCommitResult("patch", "bad", False)
    assert PatchBranchPlan("patch", "main", "karakana/patch", "main", True).can_create
