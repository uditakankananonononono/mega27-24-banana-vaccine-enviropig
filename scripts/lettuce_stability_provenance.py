"""Verify reported lettuce oral-antigen handling/stability claims in source XML.

These are author-reported group summaries, not independent measurements or a digestion assay.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/pmc3088802.xml';s=BeautifulSoup(p.read_text(),'xml')
paras=[x.get_text(' ',strip=True) for x in s.find_all('p')]
claims={
 'one_year_retention_text':'stability (95–98%) of S-HBsAg content for at least one year of room temperature storage',
 'processing_loss_text':'at least 90% decrease of S-HBsAg VLPs content',
 'assay_repeats_text':'from three (lettuce leaves) or ten (lyophilized tissue and tablets) repeated assays',
 'tablet_content_text':'2.3 μg/unit of tablets',
}
for key,phrase in claims.items():
 matches=[x for x in paras if phrase in x.replace('\u00a0',' ')]
 assert matches,(key,phrase)
 claims[key]={'phrase':phrase,'source_paragraph':matches[0]}
out={'source':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3088802/',
 'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'claims':claims,
 'interpretation':'The same article reports substantial process-stage loss of assembled protein but high one-year retention of remaining protein in stored powder/tablet. These have different denominators and cannot be collapsed into one effective intestinal dose.',
 'limits':['Author-reported ranges, not independently remeasured individual tablet/plant assay values','Repeated ELISA assays are not independent plant or digestion biological replicates','One paper and antigen system; no cross-study matched comparator or new oral-dose discovery','This analysis does not prescribe manufacturing steps or antigen design'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
