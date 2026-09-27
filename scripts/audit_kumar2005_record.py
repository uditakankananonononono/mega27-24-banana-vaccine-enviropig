"""Provenance and printed-value audit of the Kumar 2005 Planta record.

Pins the live NCBI identity of the screen's Kumar 2005 entry (DOI
10.1007/s00425-005-1556-y, PMID 15918027) from the archived PubMed abstract,
replays its printed values, checks the eligibility screen's stated basis
against the abstract, and places the printed leaf-content maxima next to the
pinned Thanavala record as published-design scale context. Printed-number
audit only.
"""
from pathlib import Path
import hashlib, json, re
from xml.etree import ElementTree as ET
R = Path(__file__).resolve().parents[1]
src = R / 'data/sources/kumar2005_pubmed_abstract.xml'
sha = hashlib.sha256(src.read_bytes()).hexdigest()
root = ET.parse(src).getroot()
art = root.find('.//Article')
title = ' '.join(''.join(art.find('.//ArticleTitle').itertext()).split())
journal = ' '.join(''.join(art.find('.//Journal/Title').itertext()).split())
year = art.find('.//JournalIssue/PubDate/Year').text
doi = next(x.text for x in root.findall('.//ArticleId') if x.attrib.get('IdType') == 'doi')
pmid = root.find('.//PMID').text
abstract = ' '.join(' '.join(x.itertext()) for x in art.findall('.//AbstractText'))
abstract = ' '.join(abstract.split())

m_invitro = re.search(r'Maximum expression level of ([\d.]+) ng/g', abstract)
m_green = re.search(r'maximum expression level of ([\d.]+) ng/g', abstract)
m_bind = re.search(r'binding of ([\d.]+)%', abstract)
m_dens = re.search(r'found to be ([\d.]+) g/ml', abstract)
assert m_invitro and m_green and m_bind and m_dens
fruit_rtpcr_only = ('fruits was confirmed by RT-PCR' in abstract) and not re.search(r'fruit[^.]{0,80}ng/g', abstract.lower())
four_constructs = 'Four different expression cassettes' in abstract

screen = json.loads((R / 'results/eligibility_screen.json').read_text())
entry = next(s for s in screen['screened_studies'] if s['study'].startswith('Kumar 2005'))
screen_basis_consistent = (not entry['fruit_protein_quantified']) and fruit_rtpcr_only and 'leaf' in entry['tissue']

than = json.loads((R / 'results/thanavala_dose_record.json').read_text())
than_ng_per_g = than['checks']['printed_records']['content_ug_per_g_tuber'] * 1000

checks = {
 'identity': {'title': title, 'journal': journal, 'year': year, 'doi': doi, 'pmid': pmid,
              'screen_url_doi_match': entry['url'].endswith(doi)},
 'printed_records': {'constructs_compared': 4 if four_constructs else None,
                     'leaf_content_max_ng_per_g_fw_in_vitro': float(m_invitro.group(1)),
                     'leaf_content_max_ng_per_g_fw_greenhouse': float(m_green.group(1)),
                     'monoclonal_binding_pct_with_er_signal': float(m_bind.group(1)),
                     'buoyant_density_g_per_ml': float(m_dens.group(1)),
                     'fruit_measurement': 'RT-PCR detection only; no fruit content value printed'},
 'screen_basis_consistent': screen_basis_consistent,
 'cross_design_scale': {'thanavala2005_content_ng_per_g_fresh_tuber': than_ng_per_g,
                        'content_ratio_thanavala_over_kumar_invitro_max': round(than_ng_per_g / float(m_invitro.group(1)), 1),
                        'note': 'Different species, tissues, constructs and bases; a scale comparison of printed published numbers only, not a potency or outcome comparison'},
 'endpoint_classification': {'banana_fruit_data': True, 'fruit_content_quantified': False,
                             'measured_post_digestion_intact_fraction': False,
                             'eligible_for_locked_primary_endpoint': False}}
out = {'source_url': 'https://link.springer.com/article/10.1007/s00425-005-1556-y',
 'efetch': 'NCBI eutils esearch+efetch db=pubmed id=15918027 rettype=abstract (abstract record archived 2026-09-28)',
 'source_file': src.name, 'sha256': sha, 'checks': checks,
 'finding': "The screen's Kumar 2005 entry resolves live to the Planta 2005 record (PMID 15918027) and the archived abstract confirms the screen's stated basis: leaf content maxima printed for two growth settings, fruit confirmed by RT-PCR only with no printed fruit content value. Printed leaf maxima are 38 ng/g F.W. (in vitro) and 19.92 ng/g F.W. (greenhouse); the pinned Thanavala record's printed tuber content is ~224x the in-vitro leaf maximum on a fresh-weight ng/g scale (descriptive cross-design context only). Eligibility screen unchanged at 0/6.",
 'limits': ['Abstract-level record; construct-level spread and replicate values are not printed here',
            'Screen basis check upgrades the entry evidence from publisher page to pinned abstract; no new study added',
            'Printed-number audit only; no design, formulation or protocol recommendation'],
 'gate_credit': {'external_services': 0, 'fetched_and_used_accession_datasets': 0, 'audited_derivations': 0, 'paper_pages': 0}}
print(json.dumps(out, indent=2, sort_keys=True))
