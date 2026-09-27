"""Separate source's five-line display range from the one administered line."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/chan2013_published_table1.json'
x=json.loads(p.read_text())
line4=next(row for row in x['rows'] if row[0]==4)
assert len(x['rows'])==5
implied=50*line4[3]/1000
assert round(implied,2)==12.88 and round(implied,1)==12.9
out={'source_url':x['source_url'],'extract_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'published_line_count':5,'administered_line':4,'administered_line_fresh_leaf_ng_per_g_mean':line4[3],
     'author_reported_administered_mass_g':50,'calculated_administered_line_content_ug':round(implied,2),
     'article_administered_line_stated_content_ug':12.9,
     'article_all_five_line_context_range_ug':[7.7,12.9],
     'finding':'The published source’s 7.7–12.9 ug figure is a five-line expression-derived range; the animal experiment used one selected banana leaf line (no. 4) with 50 g and an author-stated 12.9 ug per administration. Five line means must not be passed off as five tested oral doses or digestion replicates.',
     'scope_note':'The source’s article text was read on 2026-09-28. Its experimental-procedures paragraph explicitly identifies line no. 4; this script replays the numeric consistency from archived Table 1 only, since the original article HTML prose is not stored byte-for-byte in the repository.',
     'limits':['Not an independently measured per-animal antigen consumption distribution',
               'The Table 1 five-line range was not randomized among the animal groups',
               'No banana fruit mass, post-digestion intact fraction, vaccine efficacy comparison, sequence or construct advice'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
