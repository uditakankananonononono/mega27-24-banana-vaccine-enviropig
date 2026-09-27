from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_nonvaccine_field_proxy():
    result=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_banana_nonvaccine_field_proxy.py')],text=True))
    assert result==json.loads((R/'results/banana_nonvaccine_field_proxy.json').read_text())
    assert result['published_wildtype_control_extremes']['ratio_of_extremes']==8.1
    assert result['gate_credit']['fetched_and_used_accession_datasets']==0
