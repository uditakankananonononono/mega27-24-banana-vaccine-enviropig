# PMC549291 dose-record provenance and screen-label correction, 2026-09-27

The eligibility screen lists "Tacket et al., 2004" linked to [PMC549291](https://pmc.ncbi.nlm.nih.gov/articles/PMC549291/). A live NCBI lookup (esummary + efetch, archived abstract XML with SHA-256 pinned in `results/thanavala_dose_record.json`) resolves that PMCID to **Thanavala et al., PNAS 2005**, "Immunogenicity in humans of an edible vaccine for hepatitis B" (PMID 15728371, DOI 10.1073/pnas.0409899102). The screen's citation label is wrong and should be read as this record; its endpoint classification stands unchanged under either authorship - human serum antibody titre responder counts are not banana fruit data and not a measured post-digestion intact fraction, so the screen stays 0/6. The publisher bars full-text XML download, so this is an abstract-level archive.

**Printed dose record.** Potatoes accumulated the antigen at approximately 8.5 ug/g of tuber (the abstract prints the approximation marker), administered as 100 g doses. Implied content per dose is therefore approximately 850 ug, inheriting the approximation.

**Arithmetic replay.** Both printed responder percentages round correctly: 10/16 = 62.5% exactly (three-dose arm) and 9/17 = 52.94%, printed as 52.9% (two-dose arm); zero responders among controls (control-arm size not printed in the abstract). The two printed treated arms total 33 volunteers.

**Cross-design scale context.** Next to the previously pinned [Pelosi 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3527624/) record (300 ug/g dry weight, 5.7 mg available per 19 g dose), this record's printed per-gram content is 35.3x lower and its implied per-dose content (0.85 mg) is 6.7x lower. Species, tissue, dry-vs-fresh basis and decade all differ; this is a scale comparison of printed published numbers for the dose-variability evidence base, not a potency or outcome comparison.

The script replays identity, ratios and scale arithmetic from the archived record and the pinned Pelosi JSON, covered by a hermetic test. No new eligibility, no comparator win, no discovery, no gate credit.
