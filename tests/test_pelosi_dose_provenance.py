import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_pelosi_dose_provenance():
 d=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_pelosi_dose_provenance.py')],text=True))
 assert d==json.loads((R/'results/pelosi_dose_provenance.json').read_text())
 assert d['arithmetic_check']['covers_stated_5mg_delivery'] is True
 assert d['endpoint_classification']['eligible_for_locked_primary_endpoint'] is False
 assert all(v==0 for v in d['gate_credit'].values())
