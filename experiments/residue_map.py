"""Per-residue conservation map: reference spike positions vs 5 variants."""
import json, sys
sys.path.insert(0, "src")
from Bio import Align
from Bio.Align import substitution_matrices

def read_fasta(p):
    return "".join(l.strip() for l in open(p) if not l.startswith(">"))

ref = read_fasta("data/variants/wuhan.fasta")
variants = {v: read_fasta(f"data/variants/{v}.fasta")
            for v in ("alpha", "delta", "omicron_BA1", "omicron_BA2", "omicron_BA5")}
al = Align.PairwiseAligner()
al.substitution_matrix = substitution_matrices.load("BLOSUM62")
al.open_gap_score, al.extend_gap_score, al.mode = -10, -0.5, "global"
rows = []
for name, vseq in variants.items():
    aln = al.align(ref, vseq)[0]
    pos = {}
    for (rs, re), (vs, ve) in zip(*aln.aligned):
        for k in range(re - rs):
            pos[rs + k] = vseq[vs + k]
    rows.append(pos)
out = []
for i, aa in enumerate(ref):
    rec = {"pos": i + 1, "ref": aa}
    for name in variants:
        rec[name] = rows[list(variants).index(name)].get(i, "-")
    out.append(rec)
json.dump(out, open("results/residue_map.json", "w"))
# windowed stats
import numpy as np
W = 50
wins = []
for s in range(0, len(ref) - W + 1, W):
    row = {"start": s + 1}
    for name in variants:
        ident = sum(1 for r in out[s:s+W] if r[name] == r["ref"]) / W
        row[name] = round(ident, 3)
    wins.append(row)
json.dump(wins, open("results/window_conservation.json", "w"), indent=1)
print(len(out), "positions,", len(wins), "windows")
print("least conserved windows:", sorted(wins, key=lambda r: r["omicron_BA2"])[:3])
