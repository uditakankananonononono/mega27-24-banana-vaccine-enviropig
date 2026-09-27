import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_chan2013_print_layer():
    result=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_chan2013_leaf_variation.py')],text=True))
    assert result==json.loads((ROOT/'results/chan2013_leaf_variation.json').read_text())
    assert result['implied_50g_mass_range_ug']==[7.71,12.88]
    assert result['line_mean_max_over_min']==1.6706
