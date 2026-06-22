from karakana.requirements.issues import generate_issues
from karakana.requirements.prd import generate_prd
from karakana.requirements.readiness import check_readiness
from karakana.requirements.schemas import RequirementSource
from karakana.requirements.store import RequirementsStore
from karakana.requirements.stories import generate_stories


def test_requirements_store_save_load_list_latest(tmp_path):
    store = RequirementsStore(tmp_path)
    prd = generate_prd(RequirementSource(source_type="note"), "Add requirements artifacts.")
    prd_path = store.save_prd(prd)
    stories = generate_stories(prd)
    issues = generate_issues(prd, stories)
    store.save_stories(prd.req_id, stories)
    store.save_issues(prd.req_id, issues)
    store.save_readiness(check_readiness(prd))

    assert prd_path.exists()
    assert store.load_prd(prd.req_id).req_id == prd.req_id
    assert store.load_stories(prd.req_id)[0].req_id == prd.req_id
    assert store.load_issues(prd.req_id)[0].req_id == prd.req_id
    assert store.load_readiness(prd.req_id).req_id == prd.req_id
    assert store.latest() == prd.req_id
    assert prd.req_id in store.list_requirements()
