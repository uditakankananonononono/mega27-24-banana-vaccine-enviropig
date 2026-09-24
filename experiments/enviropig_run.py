"""Run the Enviropig mass balance + phytase pH profile, save results + figure."""
import json, os, sys
import numpy as np
sys.path.insert(0, "src")
from agrobio.enviropig import manure_phosphorus, ph_activity, phytate_hydrolysis

def main():
    abs_no, exc_no = manure_phosphorus(with_phytase=False)
    abs_yes, exc_yes = manure_phosphorus(with_phytase=True)
    reduction = (exc_no - exc_yes) / exc_no
    phs = np.linspace(1.5, 7.5, 25)
    prof = [ph_activity(float(p)) for p in phs]
    # compartment sweep: vary enzyme dose
    doses = np.linspace(0.05, 0.8, 16)
    red_vs_dose = []
    for d in doses:
        _, e0 = manure_phosphorus(with_phytase=False)
        _, e1 = manure_phosphorus(enzyme_units=float(d), with_phytase=True)
        red_vs_dose.append((e0 - e1) / e0)
    out = dict(diet_p_g=5.0, phytate_fraction=0.65,
               absorbed_no_phytase=abs_no, excreted_no_phytase=exc_no,
               absorbed_with_phytase=abs_yes, excreted_with_phytase=exc_yes,
               manure_P_reduction=float(reduction),
               published_band=[0.20, 0.60],
               within_published_band=bool(0.20 <= reduction <= 0.60),
               dose_sweep=dict(doses=doses.tolist(), reductions=red_vs_dose))
    os.makedirs("results", exist_ok=True)
    json.dump(out, open("results/enviropig.json", "w"), indent=1)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(phs, prof); ax[0].set_xlabel("gut pH"); ax[0].set_ylabel("relative AppA activity")
    ax[0].set_title("AppA phytase twin-peak pH profile")
    ax[1].plot(doses, red_vs_dose); ax[1].axhline(0.2, ls="--", c="gray"); ax[1].axhline(0.6, ls="--", c="gray")
    ax[1].set_xlabel("salivary phytase dose (units)"); ax[1].set_ylabel("manure-P reduction")
    ax[1].set_title("Dose response vs published 20-60% band")
    fig.tight_layout(); fig.savefig("results/figures/enviropig.png", dpi=150)
    print(json.dumps({k: v for k, v in out.items() if k != "dose_sweep"}, indent=1))

if __name__ == "__main__":
    main()
