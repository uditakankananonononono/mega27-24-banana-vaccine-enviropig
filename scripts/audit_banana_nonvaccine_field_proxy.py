"""Screen published fruit-variability fields without treating carotenoid as vaccine antigen."""
from pathlib import Path
from lxml import etree
import hashlib,json
R=Path(__file__).resolve().parents[1]
ids=['PMC5362681','PMC13110172']
roots=[etree.parse(str(R/'data/sources'/f'{id.lower()}.xml')) for id in ids]
texts=[' '.join(' '.join(p.itertext()) for p in root.xpath('//p')) for root in roots]
assert '244 transgenic lines' in texts[0] and 'single plant was established' in texts[0]
assert '1.0' in texts[0] and '8.1' in texts[0] and 'bunch filling time' in texts[0]
assert 'three successive generations' in texts[1] and '27 independent transgenic and five wild‐type lines' in texts[1]
assert '4 biological replicates over 3 generations' in texts[1]
source=[{'url':f'https://pmc.ncbi.nlm.nih.gov/articles/{id}/',
         'europe_pmc_xml_url':f'https://www.ebi.ac.uk/europepmc/webservices/rest/{id}/fullTextXML',
         'sha256':hashlib.sha256((R/'data/sources'/f'{id.lower()}.xml').read_bytes()).hexdigest(),
         'title':' '.join(root.xpath('//article-title')[0].itertext())} for id,root in zip(ids,roots)]
out={'sources':source,'published_wildtype_control_extremes':{'min_microgram_per_g_dry_weight_beta_carotene_equivalents':1.0,
       'max_microgram_per_g_dry_weight_beta_carotene_equivalents':8.1,
       'ratio_of_extremes':8.1,'scope':'wild-type fruit across two field trials and different harvest months, not paired plants or vaccine dose'},
     'field_design':{'first_trial_transgenic_lines':244,'first_trial_plants_per_line':1,
                     'second_trial_transgenic_lines':27,'second_trial_wildtype_lines':5,
                     'later_trial_replication':'ten field-derived sucker plants per line in randomized plots; 3 successive generations assessed'},
     'finding':'These published banana fruit studies show a measurable fruit trait and field/season differences, but their trait is pro-vitamin A carotenoids, not orally delivered vaccine antigen. A variability predictor cannot use those fruit values as antigen or digestion outcomes.',
     'limits':['The 1.0 and 8.1 values are wild-type fruit means from different trials/months; their ratio is descriptive across contexts, not an individual fruit coefficient of variation.',
               'Do not substitute carotenoid HPLC for antigen ELISA, post-digestion antigen fraction or immune response.',
               'The later trial revisits selected lines and is not an independent validation set for a vaccine-antigen prediction.',
               'No construct/sequence/delivery-system recommendation, antigen comparator, accession payload or project gate credit.'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
