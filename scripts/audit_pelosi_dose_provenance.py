"""Pin and replay the published Pelosi 2012 dose records and their denominators.

Measurement-provenance audit only: no antigen, construct, sequence or protocol content.
"""
from pathlib import Path
import hashlib, json, re
R=Path(__file__).resolve().parents[1]
xml=R/'data/sources/pmc3527624.xml'
raw=xml.read_bytes()
text=re.sub(r'\s+',' ',raw.decode('utf-8'))
claims={
 'batch_content':'hairy root and leaf vaccine batches accumulated 300',
 'dose_statement':'each dose was sufficient to deliver 5 mg',
 'group_sizes':'randomly assigned into four groups of 2',
 'formulation_mass':'mixing 19 g freeze-dried plant material with 200 ml',
 'elisa_basis':'calculated against a <italic toggle="yes">Pichia pastoris</italic>-made rLTB (Sigma-Aldrich) standard',
 'schedule':'immunised on days 0, 14 and 28 followed by a boost dose on day 38',
}
found={k:(v in text) for k,v in claims.items()}
assert all(found.values()), found
material_g=19.0
content_ug_per_g=300.0
computed_ug=material_g*content_ug_per_g
result={'source_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3527624/',
 'europepmc_xml_url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3527624/fullTextXML',
 'source_file':xml.name,'sha256':hashlib.sha256(raw).hexdigest(),
 'printed_records':{
  'batch_content_ug_per_g_dwt':300,'batch_content_applies_to':['hairy root','leaf'],
  'stated_delivery_per_dose_mg':5,'formulation_freeze_dried_material_g':19,
  'formulation_emulsion_ml':200,'groups':4,'animals_per_group_printed':'2-5',
  'quantification_basis':'capture ELISA against a commercial recombinant standard'},
 'arithmetic_check':{'material_g_x_content_ug_per_g':computed_ug,
  'computed_mg_available_per_dose':computed_ug/1000.0,
  'covers_stated_5mg_delivery':computed_ug>=5000,
  'margin_percent_over_stated':round((computed_ug/5000.0-1)*100,2)},
 'endpoint_classification':{'measured_post_digestion_intact_antigen_fraction':False,
  'banana_fruit_data':False,'fruit_to_fruit_replicates':False,
  'outcome_type':'animal immune readouts (antibody titres), not digestion-survival measurements',
  'eligible_for_locked_primary_endpoint':False},
 'limits':['Printed dose/expression records with denominators; the paper reports immune outcomes, not measured intact-antigen survival through digestion',
  'Both batches printed at one identical content value, so no between-batch variability can be computed from this source',
  'Animal groups of 2-5 are biological replicates of animals, not plant-to-plant or digestion-to-digestion replicates',
  'Audit of published numbers only; no design, formulation or protocol recommendation'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
