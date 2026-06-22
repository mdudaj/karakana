from karakana.patch.branch import plan_patch_branch


def test_patch_branch_dry_run(tmp_path):
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    plan = plan_patch_branch(tmp_path, "patch")

    assert plan.proposed_branch == "karakana/patch-patch"
    assert plan.can_create


def test_patch_branch_refuses_main_name(tmp_path):
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    plan = plan_patch_branch(tmp_path, "patch", name="main")

    assert plan.can_create is False
