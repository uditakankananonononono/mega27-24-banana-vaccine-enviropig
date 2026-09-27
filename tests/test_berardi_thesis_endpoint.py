import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_thesis_numeric_gi_result_not_fruit_holdout():
 actual=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/audit_berardi_thesis_endpoint.py')],text=True))
 assert actual==json.loads((ROOT/'results/berardi_thesis_endpoint_audit.json').read_text())
 c=actual['classification'];v=actual['reported_numeric_observations']
 assert c['published_numeric_gi_assay'] and c['vaccine_antigen']
 assert not c['eligible_for_locked_held_out_primary_endpoint']
 assert not c['banana_fruit']
 assert v['coated_tablet_after_gastric_then_intestinal_native_vlp_release_pct_mean']==87.1
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
