import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_administered_line():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_chan2013_administered_line.py')],text=True))
 assert x==json.loads((ROOT/'results/chan2013_administered_line.json').read_text())
 assert x['administered_line']==4 and x['calculated_administered_line_content_ug']==12.88
