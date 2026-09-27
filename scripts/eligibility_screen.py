"""Published endpoint compatibility screen; never substitutes indirect endpoints for measured dose."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=R/'data/sources/berardi2017_accepted.pdf'
spirulina=R/'data/sources/pmc9200632.xml'
studies=[
 {'study':'Kumar 2005 banana expression','url':'https://link.springer.com/article/10.1007/s00425-005-1556-y','tissue':'banana leaf and fruit','fruit_protein_quantified':False,'numeric_post_digestion_intact_fraction':False,'within_fruit_batch_replicates':False,'basis':'Publisher abstract: leaf antigen maxima in two growth settings; fruit RT-PCR only in accessible text'},
 {'study':'Thanavala 2005 human potato trial','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC549291/','tissue':'potato','fruit_protein_quantified':False,'numeric_post_digestion_intact_fraction':False,'within_fruit_batch_replicates':False,'basis':'Oral dose/immunogenicity, not matched banana fruit and digestion survival'},
 {'study':'Pelosi 2012 sheep plant tissue comparison','url':'https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0052907','tissue':'root and leaf','fruit_protein_quantified':False,'numeric_post_digestion_intact_fraction':False,'within_fruit_batch_replicates':False,'basis':'Published immune response across tissues/formulations, not measured intact post-digestion fraction'},
 {'study':'Berardi 2017 purified plant antigen GI stability','url':'https://kar.kent.ac.uk/78842/','tissue':'purified from tobacco plant','fruit_protein_quantified':False,'numeric_post_digestion_intact_fraction':False,'within_fruit_batch_replicates':False,'basis':'Accepted manuscript describes gel, blot and imaging outcomes in simulated/pig fluids; no numeric replicate-level intact-fraction table recovered for preregistered endpoint'},
 {'study':'Lakshmi 2013 lettuce CTB-ESAT6 capsule','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3552857/','tissue':'lettuce and tobacco leaves','fruit_protein_quantified':False,'numeric_post_digestion_intact_fraction':False,'within_fruit_batch_replicates':False,'basis':'Expression, lyophilization storage and GM1 binding; no measured post-digestion intact fraction in source full text'},
 {'study':'Jester 2022 spirulina antibody gastric test','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9200632/','tissue':'spray-dried spirulina biomass (not banana fruit)','fruit_protein_quantified':False,'numeric_post_digestion_intact_fraction':False,'within_fruit_batch_replicates':False,'basis':'Source says >70% aa682 VHH antibody intact after 2h simulated gastric exposure within biomass, versus purified protein fully degraded after 2min; this is a therapeutic antibody, not an antigen-vaccine endpoint; no banana fruit or numeric replicate-level intact-antigen fraction table'}]
result={'screened_studies':studies,'source_pdf_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'spirulina_source_sha256':hashlib.sha256(spirulina.read_bytes()).hexdigest(),
 'spirulina_numeric_non_antigen_near_miss':'>70% encapsulated aa682 antibody intact at 2h in simulated gastric conditions; not a vaccine antigen endpoint',
 'source_pdf_url':'https://kar.kent.ac.uk/78842/1/Accepted_manuscript%20%282%29.pdf',
 'matched_primary_endpoint_studies':sum(x['numeric_post_digestion_intact_fraction'] for x in studies),
 'matched_banana_fruit_joint_studies':sum(x['tissue']=='banana fruit' and x['fruit_protein_quantified'] and x['numeric_post_digestion_intact_fraction'] and x['within_fruit_batch_replicates'] for x in studies),
 'status':'No prediction model or benchmark can be fitted to these screened studies for the locked primary outcome; this is an incomplete evidence screen, not proof no such source exists elsewhere.',
 'limits':['A paper outside this six-study screen may contain eligible data','Binary fields describe evidence recovered, not universal absence from full paywalled articles or supplemental data','Do not pool human immune readouts, sheep response, purified-particle gel readouts and banana fruit transcript signal as one dose endpoint'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
