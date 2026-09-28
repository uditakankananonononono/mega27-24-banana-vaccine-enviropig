"""Typed stage and denominator guard on archived edible-vaccine quantities."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
chan=json.loads((R/'results/chan2013_leaf_variation.json').read_text())
lettuce=json.loads((R/'results/lettuce_batch_variation.json').read_text())
# Use pinned source-audit values; never infer fruit protein from leaf transcript or potency from total antigen.
records={
 'Chan_line4':{'material':'banana_leaf','basis':'fresh','analyte':'GP5_total','stage':'expression','cohort':'Chan_line4',
              'ug_per_g':257.6/1000,'url':'https://onlinelibrary.wiley.com/doi/10.1111/pbi.12015'},
 'Pyrski_batch_IV':{'material':'lettuce_leaf','basis':'dry','analyte':'HBsAg_VLP','stage':'processed','cohort':'batch_IV',
                    'ug_per_g':29,'url':lettuce['source_url']},
 'Pyrski_total_IV':{'material':'lettuce_leaf','basis':'dry','analyte':'HBsAg_total_immunoreactive','stage':'processed','cohort':'batch_IV',
                    'ug_per_g':538,'url':lettuce['source_url']}}
assert lettuce['published_mouse_dose_ng_vlp']==50
assert next(row for row in chan['rows'] if row['published_line']==4)['fresh_leaf_ng_per_g_mean']==257.6
assert abs(lettuce['published_mouse_dose_ng_vlp']/lettuce['published_mouse_powder_mg']-29)<0.1
cases=json.loads((R/'data/stage_guard_cases.json').read_text())
out=[]
for x in cases:
 y={'case_id':x['id'],'requested_stage':x['stage'],'reported_nominal_ug':None,'intestinal_surviving_ug':None,'measured_fruit_antigen_ug':None}
 if not x['ratio_record']:y['status']='no_matched_measurement'
 else:
  r=records[x['ratio_record']]
  mismatches=[k for k in ['material','basis','analyte','stage','cohort'] if x[k]!=r[k]]
  y['mismatched_dimensions']=mismatches
  if mismatches:y['status']='blocked_mismatch'
  else:
   y['status']='permitted_nominal';y['reported_nominal_ug']=x['mass_g']*r['ug_per_g'];y['source_url']=r['url']
 assert y['status']==x['expected_status']
 out.append(y)
print(json.dumps({'source_urls':[records[k]['url'] for k in records],
 'source_audit_sha256':{'chan':hashlib.sha256((R/'results/chan2013_leaf_variation.json').read_bytes()).hexdigest(),
                        'lettuce':hashlib.sha256((R/'results/lettuce_batch_variation.json').read_bytes()).hexdigest()},
 'cases':out,'permitted_nominal_count':sum(y['status']=='permitted_nominal' for y in out),
 'blocked_mismatch_count':sum(y['status']=='blocked_mismatch' for y in out),
 'no_matched_measurement_count':sum(y['status']=='no_matched_measurement' for y in out),
 'interpretation':'Typed material, assay, stage and cohort guards refuse banana-fruit or digested-dose claims unsupported by the archived published leaf and processing data.',
 'limits':['All cases are constructed after source inspection and do not constitute a held-out benchmark.',
           'Permitted nominal values are publication arithmetic, not individual or post-digestion exposure.',
           'Only a true source-paired banana-fruit intact antigen concentration and matched digestion stage could populate the requested endpoint.',
           'Rule-based data validation and potency assays have prior art; no novel algorithm or new biological discovery is claimed.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}},indent=2,sort_keys=True))
