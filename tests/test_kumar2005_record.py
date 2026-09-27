import json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_kumar_record():
    actual = json.loads(subprocess.check_output(['python3', str(ROOT / 'scripts/audit_kumar2005_record.py')], text=True))
    assert actual == json.loads((ROOT / 'results/kumar2005_record.json').read_text())
    c = actual['checks']
    assert c['identity']['pmid'] == '15918027' and c['identity']['screen_url_doi_match']
    assert c['screen_basis_consistent']
    assert not c['endpoint_classification']['eligible_for_locked_primary_endpoint']
