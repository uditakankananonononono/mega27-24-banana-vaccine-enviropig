import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_screen_replays_and_prevents_endpoint_substitution():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/eligibility_screen.py')],text=True))
 assert actual==json.loads((R/'results/eligibility_screen.json').read_text())
 assert actual['matched_primary_endpoint_studies']==0
 assert actual['matched_banana_fruit_joint_studies']==0
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0

def test_pmc549291_identity_label_matches_archived_record():
 screen=json.loads((R/'results/eligibility_screen.json').read_text())
 ident=json.loads((R/'results/thanavala_dose_record.json').read_text())['checks']['identity']
 linked=[s for s in screen['screened_studies'] if s['url'].endswith('/PMC549291/')]
 assert len(linked)==1
 assert ident['first_author']=='Thanavala' and ident['year']=='2005'
 assert 'Thanavala 2005' in linked[0]['study']
