"""Print-layer variation audit of an already published banana-leaf table."""
from pathlib import Path
import json,statistics,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/chan2013_published_table1.json';x=json.loads(p.read_text())
assert len(x['rows'])==5 and [r[0] for r in x['rows']]==[1,2,3,4,5]
rows=[]
for line,tsp,tsp_pm,fw,fw_pm,pct in x['rows']:
    implied=50*fw/1000
    rows.append({'published_line':line,'fresh_leaf_ng_per_g_mean':fw,
                 'fresh_leaf_plus_minus_printed':fw_pm,'percent_tsp_printed':pct,
                 'implied_50g_mass_ug':round(implied,3),
                 'tsp_percent_recomputed':round(tsp/1e4,4)})
means=[r['fresh_leaf_ng_per_g_mean'] for r in rows]
range_calc=[min(r['implied_50g_mass_ug'] for r in rows),max(r['implied_50g_mass_ug'] for r in rows)]
assert abs(range_calc[0]-x['printed_dose_range_ug'][0])<.02
assert abs(range_calc[1]-x['printed_dose_range_ug'][1])<.02
out={'source_url':x['source_url'],'extract_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'source_section':x['source_section'],'tissue':x['tissue'],'rows':rows,
     'printed_plus_minus_semantics':'not assigned SD/SEM without a confirmed definition',
     'line_mean_range_ng_per_g_fresh_leaf':[min(means),max(means)],
     'line_mean_max_over_min':round(max(means)/min(means),4),
     'line_mean_cv_descriptive':round(statistics.stdev(means)/statistics.mean(means),4),
     'implied_50g_mass_range_ug':range_calc,'paper_printed_50g_range_ug':x['printed_dose_range_ug'],
     'print_arithmetic_consistent':True,
     'finding':'Five published banana-leaf line means range from 154.2 to 257.6 ng/g fresh leaf (1.6706-fold). For the published 50 g oral leaf portion, simple mass multiplication yields 7.71 to 12.88 ug, matching the paper’s rounded 7.7 to 12.9 ug. These are line-mean differences, not measured fruit-to-fruit or post-digestion variability.',
     'limits':['Published banana-leaf table, not banana fruit protein mass or digestion survival',
               'Five distinct lines are not five biological replicates of one fruit cultivar/batch; the descriptive CV is not within-fruit or plant-to-plant variance',
               'Printed plus-minus semantics and individual replicates were not recovered; no uncertainty interval or inference is attempted',
               'No design, sequence, antigen or formulation recommendation; no comparison of immune efficacy or safety'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
