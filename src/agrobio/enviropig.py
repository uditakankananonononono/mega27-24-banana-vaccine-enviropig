"""Enviropig computational study.

Real background: the Enviropig (Guelph) expressed E. coli appa phytase in
salivary glands, cutting manure phosphorus ~20-60% (Golovan et al. 2001,
Forsberg et al. 2003). This module:
1) codon-optimizes appa for Sus scrofa salivary expression,
2) models phytase catalysis vs gut pH (Michaelis-Menten + pH activity curve),
3) runs a phosphorus mass-balance: dietary phytate -> digested vs excreted.
"""
from __future__ import annotations
import math

# Sus scrofa codon usage (per-thousand, Kazusa subset used by optimizer)
PIG_CU = {
    "F": {"TTT": 42.0, "TTC": 58.0}, "L": {"TTA": 8.0, "TTG": 12.0, "CTT": 12.0,
    "CTC": 20.0, "CTA": 7.0, "CTG": 41.0},
    "I": {"ATT": 35.0, "ATC": 48.0, "ATA": 17.0}, "M": {"ATG": 100.0},
    "V": {"GTT": 18.0, "GTC": 24.0, "GTA": 11.0, "GTG": 47.0},
    "S": {"TCT": 18.0, "TCC": 22.0, "TCA": 15.0, "TCG": 6.0, "AGT": 15.0, "AGC": 24.0},
    "P": {"CCT": 28.0, "CCC": 33.0, "CCA": 27.0, "CCG": 12.0},
    "T": {"ACT": 24.0, "ACC": 36.0, "ACA": 27.0, "ACG": 13.0},
    "A": {"GCT": 26.0, "GCC": 40.0, "GCA": 22.0, "GCG": 12.0},
    "Y": {"TAT": 43.0, "TAC": 57.0}, "H": {"CAT": 41.0, "CAC": 59.0},
    "Q": {"CAA": 26.0, "CAG": 74.0}, "N": {"AAT": 45.0, "AAC": 55.0},
    "K": {"AAA": 41.0, "AAG": 59.0}, "D": {"GAT": 45.0, "GAC": 55.0},
    "E": {"GAA": 41.0, "GAG": 59.0}, "C": {"TGT": 45.0, "TGC": 55.0},
    "W": {"TGG": 100.0}, "R": {"CGT": 8.0, "CGC": 19.0, "CGA": 11.0,
    "CGG": 21.0, "AGA": 20.0, "AGG": 21.0},
    "G": {"GGT": 16.0, "GGC": 34.0, "GGA": 25.0, "GGG": 25.0},
    "*": {"TAA": 28.0, "TAG": 20.0, "TGA": 52.0},
}


def codon_optimize(peptide, cu_table=PIG_CU):
    dna = []
    for aa in peptide:
        codons = cu_table[aa]
        dna.append(max(codons, key=codons.get))
    return "".join(dna)


def cai(dna, cu_table=PIG_CU):
    aa_of = {c: aa for aa, cs in cu_table.items() for c in cs}
    logs = []
    for i in range(0, len(dna) - 2, 3):
        aa = aa_of.get(dna[i:i + 3])
        if aa is None or aa == "*":
            continue
        w = cu_table[aa][dna[i:i + 3]] / max(cu_table[aa].values())
        logs.append(math.log(max(w, 1e-6)))
    return math.exp(sum(logs) / max(len(logs), 1))


def ph_activity(ph, ph_opt=2.5, ph_opt2=5.5, width=1.6):
    """AppA phytase twin-peak pH profile (published AppA curves peak near
    pH 2.5 and 5.5); modelled as sum of two Gaussians, max normalized to 1."""
    import math as m
    g = m.exp(-((ph - ph_opt) / width) ** 2) + 0.8 * m.exp(-((ph - ph_opt2) / width) ** 2)
    norm = 1.0 + 0.8 * m.exp(-((ph_opt - ph_opt2) / width) ** 2)  # value at pH optimum
    return g / norm


def phytate_hydrolysis(ph, phytate_mmol, enzyme_units, hours, km=0.3):
    """Michaelis-Menten estimate of phytate-P released (mmol) over time."""
    act = ph_activity(ph)
    v = enzyme_units * act * phytate_mmol / (km + phytate_mmol)
    return min(phytate_mmol, v * hours)


def manure_phosphorus(diet_p_g=5.0, phytate_fraction=0.65,
                      gut_ph=(2.5, 5.0), enzyme_units=0.33, hours=6.0,
                      with_phytase=True):
    """Mass balance: returns (absorbed_g, excreted_g) of phosphorus.
    Without phytase, monogastrics absorb ~10% of phytate-P (realistic bound).
    With salivary phytase, sequential gut compartments hydrolyse phytate."""
    phytate_p = diet_p_g * phytate_fraction
    free_p = diet_p_g - phytate_p
    if not with_phytase:
        released = 0.1 * phytate_p
    else:
        released = 0.1 * phytate_p
        remaining = phytate_p - released
        for ph in gut_ph:
            r = phytate_hydrolysis(ph, remaining, enzyme_units, hours / len(gut_ph))
            released += r
            remaining -= r
    absorbed = free_p + released
    return absorbed, diet_p_g - absorbed
