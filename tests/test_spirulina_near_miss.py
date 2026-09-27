from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
import json
ROOT=Path(__file__).resolve().parents[1]

def test_numeric_therapeutic_near_miss_is_not_vaccine_endpoint():
 raw=(ROOT/'data/sources/pmc9200632.xml').read_bytes()
 text=BeautifulSoup(raw,'xml').get_text(' ',strip=True)
 assert '70% of aa682 remained intact after 2' in text
 assert 'Purified aa682 was fully degraded within 2' in text
 out=json.loads((ROOT/'results/eligibility_screen.json').read_text())
 assert out['spirulina_source_sha256']==hashlib.sha256(raw).hexdigest()
 assert len(out['screened_studies'])==6
 assert out['screened_studies'][-1]['numeric_post_digestion_intact_fraction'] is False
 assert out['matched_primary_endpoint_studies']==0
