"""Figure 1 and Table 1. Run after textbook_models.py and sdv_models.py."""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common as C
import sdv_models as S

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 10.5,
                     "axes.linewidth": .8, "axes.edgecolor": "#333",
                     "axes.spines.top": False, "axes.spines.right": False})
NAVY, ORANGE, RED, GREEN, GREY = "#1f4e79", "#e08214", "#b3202a", "#3a7d34", "#888888"

sdv_one = json.load(open(C.RES / "sdv_one_round.json"))
tb_one = json.load(open(C.RES / "textbook_one_round.json"))
sdv_rec = json.load(open(C.RES / "sdv_recursion.json"))
tb_rec = json.load(open(C.RES / "textbook_recursion.json"))

# Table 1
rows = [("Real losses", C.real)]
rows += [(f"{m} (SDV)", sdv_one[f"{m} | SDV defaults"]["median"])
         for m in ["CTGAN", "TVAE", "Gaussian copula"]]
rows += [(f"{m} (textbook, log losses)", tb_one[m]["median"])
         for m in ["GAN", "VAE", "Gaussian mixture"]]
lines = ["model | P(>x0) | h(1%) | h(0.5%) | h(0.2%) | implied gamma (1%) | largest loss"]
for name, d in rows:
    g = "--" if name == "Real losses" else (f"{d['gamma0.01']:.2f}" if np.isfinite(d["gamma0.01"])
                                            else "--")
    lines.append(f"{name} | {100 * d['ref']:.1f} | {100 * d['h0.01']:.2f} | {100 * d['h0.005']:.2f}"
                 f" | {100 * d['h0.002']:.2f} | {g} | {d['max']:.0f}")
(C.RES / "table1.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))


def median_seed(key):
    h = [r["h0.01"] for r in sdv_one[key]["runs"]]
    return int(np.argsort(h)[len(h) // 2]) + 1


# Figure 1: (a) tails after one round of training, (b) long-run estimate after recursive
# training against the fixed point that Proposition 1 implies for each model's one-round error
fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.7))
ax = axes[0]
xs = np.sort(C.x_real)
surv = 1 - np.arange(1, len(xs) + 1) / (len(xs) + 1)
ax.loglog(xs, surv, ".", ms=2.5, color="black", label="real losses")
grid = np.logspace(np.log10(C.X0 * 0.5), np.log10(xs.max() * 1.2), 200)
for name, col in [("CTGAN", RED), ("Gaussian copula", NAVY)]:
    syn = S.sdv_sample(name, C.x_real, median_seed(f"{name} | SDV defaults"))
    s_syn = np.array([np.mean(syn > g) for g in grid])
    ok = s_syn > 0
    ax.loglog(grid[ok], s_syn[ok], color=col, lw=1.8, label=f"synthetic, {name}")
for p in [C.P0, 0.01]:
    ax.axhline(p, color=GREY, lw=0.7, ls=(0, (1, 1.4)))
ax.set_xlim(1, xs.max() * 1.2); ax.set_ylim(3e-4, 1)
ax.set_xlabel("loss (DKK million)")
ax.set_ylabel("probability of a larger loss")
ax.legend(frameon=False, fontsize=8.8, loc="lower left")
ax.set_title("(a) one round of training", fontsize=10.5)

ax = axes[1]
p_real = float(np.mean(C.x_real > C.U[0.01]))
points = [(m, 1.0, sdv_rec[m], RED, "s") for m in ["CTGAN", "TVAE", "Gaussian copula"]]
points += [(m, r, tb_rec[f"{m} | m/n={r}"], NAVY, "o")
           for m in ["GAN", "VAE", "Gaussian mixture"] for r in [0.5, 1.0, 2.0]]
rows_b = []
for name, r, paths, col, mk in points:
    theta = np.mean([q["h"][0] for q in paths]) / p_real
    pred = 100 * p_real / (1 + r * (1 - theta))
    sim = 100 * np.mean([q["estimate"][-3:] for q in paths])
    rows_b.append(f"{name}, m/n = {r:g}: predicted {pred:.2f}, simulated {sim:.2f}")
    ax.plot(pred, sim, mk, color=col, ms=6, mfc="white" if r != 1.0 else col)
lim = (0.4, 1.8)
ax.plot(lim, lim, color=GREY, lw=0.9, ls=(0, (5, 3)))
ax.axhline(100 * p_real, color="black", lw=0.6, ls=(0, (1, 1.4)))
ax.axvline(100 * p_real, color="black", lw=0.6, ls=(0, (1, 1.4)))
ax.plot([], [], "s", color=RED, label="SDV tools, $m/n=1$")
ax.plot([], [], "o", color=NAVY, label="textbook models, $m/n=1$")
ax.plot([], [], "o", color=NAVY, mfc="white", label="textbook models, $m/n=0.5$ or 2")
ax.set_xlim(*lim); ax.set_ylim(*lim)
ax.set_xlabel("fixed point predicted by Proposition 1 (%)")
ax.set_ylabel("long-run estimate after retraining (%)")
ax.legend(frameon=False, fontsize=8.6, loc="upper left")
ax.set_title("(b) recursive training", fontsize=10.5)
(C.RES / "figure1_panel_b.md").write_text("\n".join(rows_b) + "\n")
print("\n".join(rows_b))
fig.tight_layout()
fig.savefig(C.FIG / "fig_evidence.pdf", metadata={"CreationDate": None})
print("saved", C.FIG / "fig_evidence.pdf")
