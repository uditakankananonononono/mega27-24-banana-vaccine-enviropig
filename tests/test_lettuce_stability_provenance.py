import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_lettuce_source_claims_replay():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/lettuce_stability_provenance.py')],text=True))
 assert actual==json.loads((R/'results/lettuce_stability_provenance.json').read_text())
 assert len(actual['claims'])==4
 assert actual['gate_credit']['audited_derivations']==0
