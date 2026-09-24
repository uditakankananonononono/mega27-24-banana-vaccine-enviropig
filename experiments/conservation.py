"""Epitope conservation sweep across real SARS-CoV-2 variant spikes.

Picks B-cell epitopes on the Wuhan-Hu-1 spike (YP_009724390.1) with the
project's property predictor, aligns five real variant spikes (Alpha, Delta,
Omicron BA.1/BA.2/BA.5, fetched from NCBI protein), and measures per-epitope
sequence identity per variant - a quantified, falsifiable survival map.
"""
import json, os, sys
sys.path.insert(0, "src")
from agrobio.vaccine import pick_epitopes, bepipred1_score
from Bio import Align
from Bio.Align import substitution_matrices

def read_fasta(p):
    return "".join(l.strip() for l in open(p) if not l.startswith(">"))

def main():
    ref = read_fasta("data/variants/wuhan.fasta")
    eps = pick_epitopes(ref, n=5, length=15, min_gap=10)
    variants = {v: read_fasta(f"data/variants/{v}.fasta")
                for v in ("alpha", "delta", "omicron_BA1", "omicron_BA2", "omicron_BA5")}
    aligner = Align.PairwiseAligner()
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -0.5
    aligner.mode = "global"

    out = {"reference": "YP_009724390.1", "epitopes": []}
    for e in eps:
        i0, i1 = e["start"], e["start"] + 15
        ep_seq = ref[i0:i1]
        row = {"start": i0, "end": i1, "seq": ep_seq, "score": e["score"], "variants": {}}
        for name, vseq in variants.items():
            aln = aligner.align(ref, vseq)[0]
            # map ref positions -> variant positions via aligned blocks
            (r_blocks, v_blocks) = aln.aligned
            pos = {}
            for (rs, re), (vs, ve) in zip(r_blocks, v_blocks):
                for k in range(re - rs):
                    pos[rs + k] = vs + k
            if i0 in pos and (i1 - 1) in pos:
                a, b = pos[i0], pos[i1 - 1] + 1
                v_ep = vseq[a:b]
                ident = sum(1 for x, y in zip(ep_seq, v_ep) if x == y) / 15.0
            else:
                v_ep, ident = None, 0.0
            rescore = None if (v_ep is None or "X" in v_ep) else sum(bepipred1_score(v_ep)) / 15.0
            row["variants"][name] = {"seq": v_ep, "identity": round(ident, 3),
                                     "rescore": None if rescore is None else round(rescore, 3)}
        out["epitopes"].append(row)
        print(row["start"], ep_seq, {k: v["identity"] for k, v in row["variants"].items()})
    os.makedirs("results", exist_ok=True)
    json.dump(out, open("results/conservation.json", "w"), indent=1)
    print("saved results/conservation.json")

if __name__ == "__main__":
    main()
