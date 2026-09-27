import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_thanavala_dose_record():
 d=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_thanavala_dose_record.py')],text=True))
 assert d==json.loads((R/'results/thanavala_dose_record.json').read_text())
 c=d['checks']
 assert c['identity']['label_matches_live_record'] is False
 assert c['identity']['first_author']=='Thanavala' and c['identity']['year']=='2005'
 pr=c['printed_records']
 assert pr['content_ug_per_g_tuber']==8.5 and pr['dose_tuber_g']==100
 assert pr['content_marked_approximate'] is True
 assert c['arithmetic']['both_arm_percentages_round_correctly'] is True
 assert c['arithmetic']['implied_content_per_dose_ug']==850.0
 assert c['arithmetic']['treated_volunteers_in_printed_arms']==33
 assert c['cross_design_scale']['content_ratio_pelosi_over_this']==35.29
 assert c['endpoint_classification']['eligible_for_locked_primary_endpoint'] is False
 assert all(v==0 for v in d['gate_credit'].values())
