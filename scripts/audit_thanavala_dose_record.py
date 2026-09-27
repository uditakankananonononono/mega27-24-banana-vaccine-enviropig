"""Provenance and dose-arithmetic audit of the published PMC549291 record.

Pins the live NCBI identity of PMC549291 (resolves to Thanavala et al., PNAS
2005, not the 'Tacket et al., 2004' label used in the repo's eligibility
screen), replays the printed abstract ratios/percentages, and places the
printed per-gram content next to the previously pinned Pelosi 2012 record as
published-design dose-scale context. Printed-number audit only.
"""
from pathlib import Path
import hashlib, json, re
from xml.etree import ElementTree as ET
R=Path(__file__).resolve().parents[1]
src=R/'data/sources/pmc549291_abstract.xml'
sha=hashlib.sha256(src.read_bytes()).hexdigest()
root=ET.parse(src).getroot()
title=' '.join(''.join(root.find('.//article-title').itertext()).split())
authors=[(a.findtext('surname') or '') for a in root.findall('.//contrib-group/contrib/name')]
year=root.find('.//pub-date/year').text
journal=' '.join(''.join(root.find('.//journal-title').itertext()).split())
abstract=' '.join(' '.join(root.find('.//abstract').itertext()).split())
doi=next(x.text for x in root.findall('.//article-id') if x.attrib.get('pub-id-type')=='doi')

# Printed abstract numbers
m_content=re.search(r'([\d.]+)\s*\S?g/g of potato tuber',abstract)
m_dose=re.search(r'doses of (\d+) g of tuber',abstract)
m3=re.search(r'(\d+) of (\d+) volunteers \(([\d.]+)%\) who ate three doses',abstract)
m2=re.search(r'(\d+) of (\d+) volunteers \(([\d.]+)%\) who ate two doses',abstract)
content_ug_per_g=float(m_content.group(1)); dose_g=int(m_dose.group(1))
arms={'three_doses':{'responders':int(m3.group(1)),'n':int(m3.group(2)),'printed_pct':float(m3.group(3))},
      'two_doses':{'responders':int(m2.group(1)),'n':int(m2.group(2)),'printed_pct':float(m2.group(3))}}
for a in arms.values():
    a['computed_pct']=round(100*a['responders']/a['n'],2)
    a['rounds_to_printed']=round(100*a['responders']/a['n'],1)==a['printed_pct']
approx='≈' in abstract.split('g of potato tuber')[0][-40:]

pelosi=json.loads((R/'results/pelosi_dose_provenance.json').read_text())
pelosi_ug_per_g=pelosi['printed_records']['batch_content_ug_per_g_dwt']
pelosi_mg_per_dose=pelosi['arithmetic_check']['computed_mg_available_per_dose']

checks={
 'identity':{'title':title,'journal':journal,'year':year,'doi':doi,'first_author':authors[0],
   'screen_doc_label':'Tacket et al., 2004','label_matches_live_record':False,
   'note':"NCBI esummary/efetch resolve PMC549291 to Thanavala et al., PNAS 2005 (PMID 15728371); the eligibility screen's 'Tacket et al., 2004' citation label does not match the linked record. The screen's endpoint classification is unaffected: the record is human immune-outcome data, not banana fruit and not a measured post-digestion intact fraction, under either authorship."},
 'printed_records':{'content_ug_per_g_tuber':content_ug_per_g,'content_marked_approximate':approx,
   'dose_tuber_g':dose_g,'arms':arms,
   'controls_responders':'none (count not printed in abstract)'},
 'arithmetic':{
   'both_arm_percentages_round_correctly':all(a['rounds_to_printed'] for a in arms.values()),
   'implied_content_per_dose_ug':content_ug_per_g*dose_g,
   'implied_content_per_dose_basis':'approximate: printed content carries a ≈ marker in the abstract',
   'treated_volunteers_in_printed_arms':sum(a['n'] for a in arms.values())},
 'cross_design_scale':{
   'pelosi2012_content_ug_per_g_dwt':pelosi_ug_per_g,
   'this_record_content_ug_per_g_fresh_tuber':content_ug_per_g,
   'content_ratio_pelosi_over_this':round(pelosi_ug_per_g/content_ug_per_g,2),
   'pelosi2012_available_mg_per_dose':pelosi_mg_per_dose,
   'this_record_implied_mg_per_dose':round(content_ug_per_g*dose_g/1000,3),
   'note':'Different species, tissues, dry-vs-fresh bases and decades; a scale comparison of printed published numbers only, not a potency or outcome comparison'},
 'endpoint_classification':{'banana_fruit_data':False,'measured_post_digestion_intact_antigen_fraction':False,
   'fruit_to_fruit_replicates':False,'outcome_type':'human serum antibody titre responders (aggregate counts)',
   'eligible_for_locked_primary_endpoint':False}}
out={'source_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC549291/',
 'efetch':'NCBI eutils efetch db=pmc id=549291 rettype=abstract (publisher bars full-text XML; abstract record archived)',
 'source_file':src.name,'sha256':sha,'checks':checks,
 'limits':['Abstract-level record: the publisher does not permit full-text XML download, so methods-level detail (exact control-arm size, per-lot content spread) is not in this archive',
  'Printed content is approximate (≈ marker); implied per-dose content inherits that approximation',
  'Responder counts are aggregate printed values; no per-subject data audited',
  'Printed-number audit only; no dose, formulation or protocol recommendation'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
