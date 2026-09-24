import math
from agrobio.enviropig import (codon_optimize, cai, ph_activity,
                               phytate_hydrolysis, manure_phosphorus)

APPA_FRAG = ("MKTLLLCSLLASVNAQAGLSAPEKRSSQGYEDAGMPLGVGCDRCLNRLQKSGYINQQV"
             "DTRQNTSVVFYRLVQQLEERGGRLTPEQAGTVDTGHSPFLHNTMGFQGDGLKDLQRVE")


def test_appa_optimizes_for_pig():
    dna = codon_optimize(APPA_FRAG)
    assert abs(cai(dna) - 1.0) < 1e-9


def test_ph_profile_twin_peak():
    assert ph_activity(2.5) > 0.9
    assert ph_activity(5.5) > 0.5
    assert ph_activity(8.5) < 0.1
    assert ph_activity(2.5) > ph_activity(3.8)


def test_hydrolysis_bounded_and_positive():
    r = phytate_hydrolysis(2.5, 10.0, 4.0, 3.0)
    assert 0 < r <= 10.0
    # more enzyme -> more hydrolysis
    assert phytate_hydrolysis(2.5, 10.0, 8.0, 3.0) >= r


def test_manure_balance_conserves_mass():
    a0, e0 = manure_phosphorus(with_phytase=False)
    a1, e1 = manure_phosphorus(with_phytase=True)
    assert abs(a0 + e0 - 5.0) < 1e-9 and abs(a1 + e1 - 5.0) < 1e-9
    assert e1 < e0  # phytase cuts excretion
    reduction = (e0 - e1) / e0
    assert 0.15 < reduction < 0.75  # published range 20-60%


def test_no_phytase_low_absorption():
    a0, e0 = manure_phosphorus(diet_p_g=5.0, with_phytase=False)
    assert a0 < 5.0 * 0.5
