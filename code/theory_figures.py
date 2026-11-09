"""Figures 2-5: reported spread by model version, long-run spreads by m/n, tail amnesia, and
the two states as a function of the number of synthetic draws."""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model import (PSTAR, BP, N_REAL, WIN_H, WIN_L, OBS_PER_YEAR, P_CUT, M_SYN, fixed_point, path,
                   simulate, maintenance_path, cutoff)

OUT = Path(__file__).resolve().parents[1] / "output" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 11,
                     "axes.linewidth": .8, "axes.edgecolor": "#333",
                     "axes.spines.top": False, "axes.spines.right": False})
NAVY, ORANGE, RED, GREEN, GREY = "#1f4e79", "#e08214", "#b3202a", "#3a7d34", "#888888"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.pdf", metadata={"CreationDate": None})
    plt.close(fig)


# Figure 2: reported spread by model version, with a simulation band for m/n = 1
T = 15
fig, ax = plt.subplots(figsize=(5.3, 3.7))
sim = simulate(N_REAL, N_REAL, T, 20000, seed=11) * BP
lo, hi = np.percentile(sim, [5, 95], axis=1)
ax.fill_between(range(T + 1), lo, hi, color=ORANGE, alpha=.16, lw=0)
ax.axhline(PSTAR * BP, color="black", lw=1.1, ls=(0, (5, 3)))
ax.text(T, PSTAR * BP + 6, "true spread", ha="right", va="bottom", fontsize=9.5)
for r, col in [(0.5, GREEN), (1.0, ORANGE), (2.0, RED)]:
    ax.plot(range(T + 1), path(r, T) * BP, color=col, lw=2.0, marker="o", ms=3.4,
            label=f"$m/n={r:g}$")
ax.set_xlim(0, T); ax.set_ylim(0, 340)
ax.set_xlabel("model version (each one retrained on the last)")
ax.set_ylabel("reported spread (basis points)")
ax.legend(frameon=False, fontsize=9.3, loc="lower right", title="synthetic-to-real ratio",
          title_fontsize=9.3)
save(fig, "fig_drift")

# Figure 3: long-run spreads of three issuers
r = np.linspace(0, 10, 401)
fig, ax = plt.subplots(figsize=(5.3, 3.7))
for ps, col in [(0.02, NAVY), (0.01, ORANGE), (0.005, RED)]:
    ax.plot(r, [fixed_point(x, ps) * BP for x in r], color=col, lw=2.2,
            label=f"true tail {100 * ps:g}%")
ax.set_xlim(0, 10); ax.set_ylim(0, 560)
ax.set_xlabel("synthetic draws per real draw ($m/n$)")
ax.set_ylabel("long-run spread (basis points)")
ax.legend(frameon=False, fontsize=9.3, loc="upper right")
save(fig, "fig_gap")

# Figure 4: a 20-year calm, then a cluster of tail events in year 45
CALM0, CALM1, CLUSTER = 10, 30, 45
ps = np.full(WIN_H + 76, PSTAR)
ps[WIN_H + CALM0:WIN_H + CALM1] = 0.005
est, kept = maintenance_path(ps, extra_events={WIN_H + CLUSTER: 9}, p_init=fixed_point(1.0))
t = np.arange(len(est))
stop = int(np.argmax(~kept))
fig, ax = plt.subplots(figsize=(5.3, 3.7))
ax.axvspan(CALM0, CALM1, color=GREY, alpha=.13, zorder=0)
ax.text((CALM0 + CALM1) / 2, 388, "long calm", ha="center", va="top", fontsize=9.5, color="#555")
ax.step(t, ps[WIN_H:] * BP, where="post", color="black", lw=1.1, ls=(0, (5, 3)))
ax.text(75, PSTAR * BP + 6, "true spread", ha="right", va="bottom", fontsize=9.5)
ax.axhline(P_CUT * BP, color=GREY, lw=1.0, ls=(0, (1, 1.4)))
ax.text(75, P_CUT * BP - 6, "cutoff", ha="right", va="top", fontsize=9, color="#555")
ax.plot(t, est * BP, color=RED, lw=2.3, zorder=4)
ax.annotate("historical data dropped", xy=(stop, est[stop] * BP), xytext=(stop + 10, 108),
            fontsize=9, color="#333", arrowprops=dict(arrowstyle="->", lw=.8, color="#333"))
ax.annotate("cluster of\ntail events", xy=(CLUSTER - 0.3, 200), xytext=(CLUSTER - 13, 315),
            fontsize=9, color="#333", arrowprops=dict(arrowstyle="->", lw=.8, color="#333"))
ax.set_xlim(0, 75); ax.set_ylim(0, 400)
ax.set_xlabel("year")
ax.set_ylabel("reported spread (basis points)")
save(fig, "fig_amnesia")

# Figure 5: long-run spreads in the two states and the cutoff, by number of synthetic draws
n_hi, n_lo = OBS_PER_YEAR * WIN_H, OBS_PER_YEAR * WIN_L
ms = np.linspace(0, 4000, 401)
rich = np.array([fixed_point(m / n_hi) for m in ms]) * BP
poor = np.array([fixed_point(m / n_lo) for m in ms]) * BP
cut = cutoff(ms) * BP
both = (poor < cut) & (cut <= rich)
fig, ax = plt.subplots(figsize=(5.3, 3.7))
ax.axvspan(ms[both][0], ms[both][-1], color=GREY, alpha=.13, zorder=0)
ax.text((ms[both][0] + M_SYN) / 2, 388, "both\nstates", ha="center", va="top", fontsize=9.5,
        color="#555")
ax.plot(ms, rich, color=NAVY, lw=2.2, label="data-rich state")
ax.plot(ms, poor, color=RED, lw=2.2, label="data-poor state")
ax.plot(ms, cut, color=GREY, lw=1.2, ls=(0, (1, 1.4)), label="cutoff")
ax.axvline(M_SYN, color="black", lw=0.8, ls=(0, (5, 3)))
ax.set_xlim(0, 4000); ax.set_ylim(0, 400)
ax.set_xlabel("synthetic draws ($m$)")
ax.set_ylabel("long-run spread (basis points)")
ax.legend(frameon=False, fontsize=9.3, loc="upper right")
save(fig, "fig_volume")
