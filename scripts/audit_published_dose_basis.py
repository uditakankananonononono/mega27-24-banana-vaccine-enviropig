"""Compare printed denominators across four archived published records, not designs."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
k=json.loads((R/'results/kumar2005_record.json').read_text())['checks']['printed_records']
t=json.loads((R/'results/thanavala_dose_record.json').read_text())['checks']['printed_records']
p=json.loads((R/'results/pelosi_dose_provenance.json').read_text())['printed_records']
l=json.loads((R/'results/lettuce_stability_provenance.json').read_text())
c=json.loads((R/'results/chan2013_leaf_variation.json').read_text())
assert k['fruit_measurement'].startswith('RT-PCR')
assert t['content_marked_approximate']
assert p['batch_content_ug_per_g_dwt']==300
assert 'one_year_retention_text' in l['claims']
records=[
 {'study':'Kumar 2005','source':'https://link.springer.com/article/10.1007/s00425-005-1556-y',
  'unit':'ng/g fresh leaf','printed_values':[k['leaf_content_max_ng_per_g_fw_in_vitro'],k['leaf_content_max_ng_per_g_fw_greenhouse']],
  'measurement_scope':'two context-specific maxima, not individual fruit masses','fruit_protein_mass_available':False,'post_digestion_intact_fraction_available':False},
 {'study':'Thanavala 2005','source':'https://pmc.ncbi.nlm.nih.gov/articles/PMC549291/',
  'unit':'ug/g fresh potato tuber (approximately)','printed_values':[t['content_ug_per_g_tuber']],
  'measurement_scope':'one approximate aggregate content value','fruit_protein_mass_available':False,'post_digestion_intact_fraction_available':False},
 {'study':'Pelosi 2012','source':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3527624/',
  'unit':'ug/g dry root or leaf','printed_values':[p['batch_content_ug_per_g_dwt']],
  'measurement_scope':'one printed value applied to both batches','fruit_protein_mass_available':False,'post_digestion_intact_fraction_available':False},
 {'study':'Pyrski lettuce','source':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3088802/',
  'unit':'author-reported stage-specific content and retention percentages','printed_values':[],
  'measurement_scope':'processing-stage and one-year storage summaries with different denominators; no individual plant values archived here',
  'fruit_protein_mass_available':False,'post_digestion_intact_fraction_available':False},
 {'study':'Chan 2013 banana leaf','source':'https://onlinelibrary.wiley.com/doi/10.1111/pbi.12015',
  'unit':'ng/g fresh banana leaf','printed_values':c['line_mean_range_ng_per_g_fresh_leaf'],
  'measurement_scope':'five distinct leaf-line means; range here is min/max, not two replicates',
  'fruit_protein_mass_available':False,'post_digestion_intact_fraction_available':False}]
out={'source_results':['results/kumar2005_record.json','results/thanavala_dose_record.json','results/pelosi_dose_provenance.json','results/lettuce_stability_provenance.json','results/chan2013_leaf_variation.json'],
     'records':records,'records_with_banana_fruit_protein_mass':sum(r['fruit_protein_mass_available'] for r in records),
     'records_with_matched_post_digestion_intact_fraction':sum(r['post_digestion_intact_fraction_available'] for r in records),
     'finding':'The five pinned published records use incompatible banana-leaf, potato-tuber, dry-tissue and process-stage denominators; none provides quantified banana-fruit protein mass paired to a post-digestion intact fraction. A pooled numeric dose-variability estimator would conflate sample units and stage losses.',
     'limits':['A bounded five-record ledger of already archived records, not a comprehensive literature search or a new measurement',
               'The lettuce source is a separate process-stage example, not an independent banana replicate',
               'No sequence, construct, formulation, antigen or protocol changes are suggested'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
