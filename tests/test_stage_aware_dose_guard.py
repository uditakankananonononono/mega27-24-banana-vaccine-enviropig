from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_stage_guard():
 x=json.loads(subprocess.check_output(['python3',str(R/'scripts/stage_aware_dose_guard.py')],text=True))
 assert x==json.loads((R/'results/stage_aware_dose_guard.json').read_text())
 assert (x['permitted_nominal_count'],x['blocked_mismatch_count'],x['no_matched_measurement_count'])==(2,3,1)
 assert abs(x['cases'][0]['reported_nominal_ug']-12.88)<1e-8
 assert all(c['intestinal_surviving_ug'] is None for c in x['cases'])
 assert x['gate_credit']['audited_derivations']==0
