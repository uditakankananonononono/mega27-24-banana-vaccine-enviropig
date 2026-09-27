"""Audit thesis GI numeric endpoints and their denominators, without design inference."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'data/sources/berardi2013_thesis.pdf'
URL='https://ueaeprints.uea.ac.uk/id/eprint/47928/1/2013BerardiAPhD.pdf'

def replay():
 raw=PDF.read_bytes()
 assert raw.startswith(b'%PDF-')
 text=subprocess.check_output(['pdftotext','-layout',str(PDF),'-'],text=True)
 markers={
  'tablet_figure_4_11_sandwich':'87.1% (± 9.6%) HBcAg VLPs were released after 6 hours of total incubation',
  'tablet_direct':'91.4% (± 4.3%) HBcAg release was',
  'tablet_control_denominator':'the total HBcAg released in the control vessels where',
  'gastric_sampling':'samples were not collected, because any',
  'microparticle_table':'Table 5.6. Microparticles encapsulation efficiency and gastro-protection (%, mean ±',
  'microparticle_6pct':'81.1 (± 4.7)                      6.0 (± 1.2)',
  'microparticle_11pct':'65.5 (± 6.9)                      11.3 (± 0.9)',
  'microparticle_2pct':'72.9 (± 4.2)                      2.7 (± 0.7)',
  'microparticle_4pct':'76.3 (± 2.4)                      4.1 (± 0.5)',
 }
 for k,phrase in markers.items():
  if phrase not in text: raise ValueError('Original PDF passage/table not found: '+k)
 return {'source':URL,'sha256':hashlib.sha256(raw).hexdigest(),'pages':299,'source_marker_checks':markers,'reported_numeric_observations':{'coated_tablet_after_gastric_then_intestinal_native_vlp_release_pct_mean':87.1,'coated_tablet_native_vlp_release_sd_percentage_points':9.6,'coated_tablet_direct_ELISA_release_pct_mean':91.4,'microparticle_post_gastric_release_pct_means':[6.0,11.3,2.7,4.1],'microparticle_post_gastric_release_sd_points':[1.2,.9,.7,.5],'microparticle_replicates_per_condition':3},'scope':'The tablet endpoint is native VLP released into simulated intestinal fluid after 2h gastric exposure, normalized to tablets kept in intestinal fluid without prior gastric exposure. Microparticle endpoint is native VLP released after a gastric step versus unstressed controls. Neither is a direct whole-sample fraction of intact antigen at the exit of digestion in banana fruit, and neither provides raw replicate values.','classification':{'published_numeric_gi_assay':True,'vaccine_antigen':True,'banana_fruit':False,'direct_post_digestion_intact_fraction_with_matched_denominator':False,'numeric_replicate_level_intact_fraction':False,'eligible_for_locked_held_out_primary_endpoint':False},'limits':['The PDF is a thesis from the same researcher as the screened 2017 manuscript; do not count it as independent of that work without comparing underlying experiments.','Reported figures are formulation-specific summary endpoints; no new construct or formulation recommendation follows, and cross-formulation ranking is not a fair model benchmark.','No biological fruit-to-fruit replicates, per-replicate intact fraction, comparable held-out publication or validation test is established.'],'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
if __name__=='__main__':print(json.dumps(replay(),sort_keys=True,indent=2))
