from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parents[1]
def test_dose_basis():
    actual=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_published_dose_basis.py')],text=True))
    assert actual==json.loads((ROOT/'results/published_dose_basis.json').read_text())
    assert len(actual['records'])==5
    assert actual['records_with_banana_fruit_protein_mass']==0
    assert actual['records_with_matched_post_digestion_intact_fraction']==0
