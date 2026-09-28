"""Audit published processing-stage dose variation, not banana fruit or gut delivery."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/pmc4209752.html'
s=BeautifulSoup(p.read_text(),'html.parser')
paras=[x.get_text(' ',strip=True) for x in s.find_all('p')]
def one(needle):
 found=[x for x in paras if needle in x]
 assert len(found)==1,(needle,len(found))
 return found[0]
batch=one('nine complete lyophilisation cycles with two cycles loaded with five separate replications')
total=one('increase in the total antigen content up to 556%')
storage=one('stored for one year at three temperatures, 4°C, 22°C, and 37°C')
mouse=one('cycle number IV with 109% preservation')
assert 'thirteen out of seventeen batches' in batch and 'mean recovery of VLPs was as high as 86%' in batch
assert '48% and 60% efficiency' in batch and 'three batches dropping below 50%' in batch
assert '192.4 μ g/g DW' in total and '1369.9 μ g/g DW' in total
assert 'to 8%' in storage and 'below 40%' in storage
assert '50\u2009ng' in mouse and '1.72\u2009mg' in mouse
out={'source_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC4209752/',
     'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'batch_quote':batch,'total_antigen_quote':total,'storage_quote':storage,'mouse_dose_quote':mouse,
     'published_complete_cycles':9,'published_subsamples_in_two_cycles':5,
     'published_batch_unit_count':17,'published_near_complete_preservation_count':13,
     'published_average_vlp_recovery_percent':86,
     'published_some_batch_recovery_below_percent':50,
     'published_total_antigen_may_increase_to_percent':556,
     'published_storage_vlp_fraction_after_three_months_at_22_or_37_c_percent':8,
     'published_mouse_dose_ng_vlp':50,'published_mouse_powder_mg':1.72,
     'mouse_dose_implied_ng_per_mg_powder':50/1.72,
     'finding':'Published lettuce S-HBsAg VLP processing has measured batch-stage variability: 13/17 units near complete preservation and mean 86% recovery, with some below 50%; total immunoreactive antigen may rise while VLP preservation is lower. This is a positive quantitative measurement-design analogue only.',
     'limits':['The nine process cycles and five subsamples in each of two cycles are nested. Seventeen units must not be treated as 17 independent production cycles.',
               'VLP structure, total antigen, and post-gastric intact antigen are distinct outcomes; no formula turns a processing recovery into a digestive-survival fraction.',
               'This source measures lettuce tissue, not banana fruit; no within-fruit variance or banana fruit antigen dose was obtained.',
               'Published summary arithmetic and heterogeneous conditions do not constitute a new strongest-comparator win, new biological discovery, or accession-level dataset.'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
