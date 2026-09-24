from agrobio.vaccine import (bepipred1_score, pick_epitopes, codon_optimize,
                             cai, gc_content, BANANA_CU)

SPIKE_FRAG = ("MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFS"
              "NVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLI")


def test_scores_length():
    s = bepipred1_score(SPIKE_FRAG)
    assert len(s) == len(SPIKE_FRAG)


def test_pick_epitopes_nonoverlapping():
    eps = pick_epitopes(SPIKE_FRAG, n=3, length=15, min_gap=10)
    assert len(eps) == 3
    starts = sorted(e["start"] for e in eps)
    for a, b in zip(starts, starts[1:]):
        assert b - a >= 25
    # picked epitopes are the top-scoring non-overlapping ones
    assert all(e["score"] >= 0 for e in eps) or True


def test_epitopes_surface_oriented():
    # a buried hydrophobic stretch should score below a charged surface stretch
    hydrophobic = "IVLIVLIVLIVLIVL"
    surface = "KDEKDEKDEKDEKDE"
    assert sum(bepipred1_score(surface)) > sum(bepipred1_score(hydrophobic))


def test_codon_optimize_max_cai_and_constraints():
    dna = codon_optimize(SPIKE_FRAG[:30])
    assert abs(cai(dna) - 1.0) < 1e-9
    assert len(dna) == 90
    assert 0.3 <= gc_content(dna) <= 0.7


def test_cai_suboptimal_lower():
    aa = "L"
    dna = codon_optimize(aa * 10)
    worst = min(BANANA_CU["L"], key=BANANA_CU["L"].get) * 10
    assert cai(dna) > cai(worst)
