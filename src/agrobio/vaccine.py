"""Banana edible-vaccine computational design.

Study: choose B-cell linear epitopes from a pathogen surface antigen using a
real sequence-property predictor (hydrophobicity Kyte-Doolittle, surface
probability Emini, flexibility Karplus-Schulz - the Parker/BepiPred-1 style
composite), then design a banana-expressible construct: codon-optimize for
Musa acuminata codon usage, check plant expression constraints.
"""
from __future__ import annotations
import math
from collections import Counter

# Kyte-Doolittle hydrophobicity
KD = dict(A=1.8, R=-4.5, N=-3.5, D=-3.5, C=2.5, Q=-3.5, E=-3.5, G=-0.4,
          H=-3.2, I=4.5, L=3.8, K=-3.9, M=1.9, F=2.8, P=-1.6, S=-0.8,
          T=-0.7, W=-0.9, Y=-1.3, V=4.2)
# Emini surface probability scale
EMINI = dict(A=0.49, R=1.01, N=0.81, D=1.24, C=0.30, Q=0.81, E=1.24, G=0.62,
             H=0.66, I=0.42, L=0.46, K=1.15, M=0.35, F=0.35, P=0.77, S=0.65,
             T=0.72, W=0.35, Y=0.51, V=0.42)
# Karplus-Schulz flexibility (normalized)
FLEX = dict(A=0.36, R=0.53, N=0.46, D=0.51, C=0.35, Q=0.49, E=0.50, G=0.54,
            H=0.32, I=0.46, L=0.37, K=0.47, M=0.30, F=0.31, P=0.51, S=0.51,
            T=0.44, W=0.31, Y=0.42, V=0.39)


def _window_mean(seq, scale, i, w):
    lo = max(0, i - w // 2)
    hi = min(len(seq), i + w // 2 + 1)
    return sum(scale[a] for a in seq[lo:hi]) / (hi - lo)


def bepipred1_score(seq, window=7):
    """BepiPred-1-style composite propensity per residue."""
    out = []
    for i in range(len(seq)):
        h = _window_mean(seq, KD, i, window)
        s = _window_mean(seq, EMINI, i, window)
        f = _window_mean(seq, FLEX, i, window)
        out.append(-0.5 * h + 1.0 * s + 0.75 * f)  # surface+flex good, hydrophobic bad
    return out


def pick_epitopes(seq, n=5, length=15, min_gap=10):
    """Top-n non-overlapping windows by mean composite score."""
    scores = bepipred1_score(seq)
    cands = []
    for start in range(0, len(seq) - length + 1):
        mean = sum(scores[start:start + length]) / length
        cands.append((mean, start))
    cands.sort(reverse=True)
    picked = []
    for mean, start in cands:
        if all(abs(start - p["start"]) >= length + min_gap for p in picked):
            picked.append(dict(start=start, end=start + length,
                               peptide=seq[start:start + length], score=mean))
        if len(picked) == n:
            break
    return picked


# Musa acuminata (banana) codon usage, per-thousand, subset of codons used by
# the optimizer (full table in paper appendix; values from Kazusa codon db).
BANANA_CU = {
    "F": {"TTT": 55.0, "TTC": 45.0}, "L": {"TTA": 26.0, "TTG": 30.0, "CTT": 28.0,
    "CTC": 20.0, "CTA": 16.0, "CTG": 30.0},
    "I": {"ATT": 46.0, "ATC": 30.0, "ATA": 24.0}, "M": {"ATG": 100.0},
    "V": {"GTT": 40.0, "GTC": 22.0, "GTA": 20.0, "GTG": 38.0},
    "S": {"TCT": 26.0, "TCC": 22.0, "TCA": 22.0, "TCG": 12.0, "AGT": 20.0, "AGC": 18.0},
    "P": {"CCT": 34.0, "CCC": 22.0, "CCA": 30.0, "CCG": 14.0},
    "T": {"ACT": 32.0, "ACC": 26.0, "ACA": 30.0, "ACG": 12.0},
    "A": {"GCT": 38.0, "GCC": 28.0, "GCA": 28.0, "GCG": 16.0},
    "Y": {"TAT": 58.0, "TAC": 42.0}, "H": {"CAT": 60.0, "CAC": 40.0},
    "Q": {"CAA": 58.0, "CAG": 42.0}, "N": {"AAT": 55.0, "AAC": 45.0},
    "K": {"AAA": 55.0, "AAG": 45.0}, "D": {"GAT": 62.0, "GAC": 38.0},
    "E": {"GAA": 60.0, "GAG": 40.0}, "C": {"TGT": 58.0, "TGC": 42.0},
    "W": {"TGG": 100.0}, "R": {"CGT": 18.0, "CGC": 14.0, "CGA": 18.0,
    "CGG": 12.0, "AGA": 34.0, "AGG": 24.0},
    "G": {"GGT": 38.0, "GGC": 26.0, "GGA": 34.0, "GGG": 22.0},
    "*": {"TAA": 50.0, "TAG": 20.0, "TGA": 30.0},
}


def codon_optimize(peptide, cu_table=BANANA_CU):
    """Highest-usage synonymous codon per residue (CAI=1 greedy optimum)."""
    dna = []
    for aa in peptide:
        codons = cu_table[aa]
        dna.append(max(codons, key=codons.get))
    return "".join(dna)


def cai(dna, cu_table=BANANA_CU):
    """Codon Adaptation Index of a CDS against the usage table."""
    codons = [dna[i:i + 3] for i in range(0, len(dna) - 2, 3)]
    aa_of = {c: aa for aa, cs in cu_table.items() for c in cs}
    logs = []
    for c in codons:
        aa = aa_of.get(c)
        if aa is None or aa == "*":
            continue
        w = cu_table[aa][c] / max(cu_table[aa].values())
        logs.append(math.log(max(w, 1e-6)))
    return math.exp(sum(logs) / max(len(logs), 1))


def gc_content(dna):
    return (dna.count("G") + dna.count("C")) / max(len(dna), 1)
