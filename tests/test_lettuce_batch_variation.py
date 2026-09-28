from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_batch_variation_replay():
 x=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_lettuce_batch_variation.py')],text=True))
 assert x==json.loads((R/'results/lettuce_batch_variation.json').read_text())
 assert x['published_batch_unit_count']==17
 assert x['published_complete_cycles']==9
 assert abs(x['mouse_dose_implied_ng_per_mg_powder']-29.07)<0.01
 assert x['gate_credit']['fetched_and_used_accession_datasets']==0
