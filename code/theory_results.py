"""Table 3 and the theoretical numbers quoted in Sections 3, 4, 6, 7, 8 and 9 and the Appendix."""
from functools import partial
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from model import (PSTAR, BP, N_REAL, GAMMA, P0, WIN_H, WIN_L, P_CUT, M_SYN, OBS_PER_YEAR,
                   h_tail_index, fixed_point, simulate, maintenance_path, maintenance_simulate,
                   detection_events, cutoff)

OUT = Path(__file__).resolve().parents[1] / "output" / "results"
OUT.mkdir(parents=True, exist_ok=True)
lines = []


def out(s=""):
    print(s)
    lines.append(s)


def pct(p):
    return f"{100 * p:.2f}"


out("# Theoretical results")
out(f"Baseline: p* = {PSTAR:.0%}, gamma = {GAMMA}, p0 = {P0:.0%}, n = {N_REAL}, spread = 2.7 x p")
out(f"Largest understatement in percentage points at p = {P0 * GAMMA ** (-1 / (GAMMA - 1)):.2%}")
out()

out("## Long-run estimate, spread and detection (Sections 3 and 6)")
for r in [0.5, 1, 2]:
    p = fixed_point(r)
    d = 1 - p / PSTAR
    out(f"m/n = {r}: estimate {p:.3%}, spread {p * BP:.0f} bp, relative bias {d:.1%}, "
        f"tail events to detect {detection_events(d):.0f} (8/delta^2 = {8 / d ** 2:.0f})")
for ps in [0.005, 0.01, 0.02]:
    out(f"p* = {ps:.1%}: spread at m/n = 0, 1, 5: "
        + ", ".join(f"{fixed_point(r, ps) * BP:.0f}" for r in [0, 1, 5]) + " bp")
for n in [2000, 200]:
    out(f"Standard deviation of the real frequency relative to p*, n = {n}: "
        f"{np.sqrt((1 - PSTAR) / (n * PSTAR)):.0%}")
out()

out("## Table 3: long-run estimate (percent) at m/n = 0.5, 1, 2")


def sim_mean(n, r, seed, rho=0.0):
    return simulate(n, int(round(r * n)), 300, 4000, seed=seed, rho=rho)[50:].mean()


def varying_ratio(r, seed=3, T=200_000):
    rng = np.random.default_rng(seed)
    p, acc = PSTAR, []
    for t in range(T):
        w = 1 / (1 + rng.uniform(0.5 * r, 1.5 * r))
        p = w * PSTAR + (1 - w) * float(h_tail_index(p))
        if t > 100:
            acc.append(p)
    return np.mean(acc)


R3 = [0.5, 1.0, 2.0]
rows = [
    ("Baseline", [fixed_point(r) for r in R3]),
    ("Simulated, n = 2,000", [sim_mean(2000, r, 21 + i) for i, r in enumerate(R3)]),
    ("Simulated, n = 200", [sim_mean(200, r, 31 + i) for i, r in enumerate(R3)]),
    ("gamma = 1.05", [fixed_point(r, h=partial(h_tail_index, gamma=1.05)) for r in R3]),
    ("gamma = 1.20", [fixed_point(r, h=partial(h_tail_index, gamma=1.20)) for r in R3]),
    ("gamma = 0.95", [fixed_point(r, h=partial(h_tail_index, gamma=0.95)) for r in R3]),
    ("p0 = 5%", [fixed_point(r, h=partial(h_tail_index, p0=0.05)) for r in R3]),
    ("p0 = 20%", [fixed_point(r, h=partial(h_tail_index, p0=0.20)) for r in R3]),
    ("Correlated real draws", [sim_mean(2000, r, 41 + i, rho=0.02) for i, r in enumerate(R3)]),
    ("Ratio varying by year", [varying_ratio(r) for r in R3]),
    ("Synthetic draws weighted one half", [fixed_point(0.5 * r) for r in R3]),
]
for name, ps in rows:
    out(f"{name:34s} " + "  ".join(pct(p) for p in ps))
for n in [2000, 200]:
    s = simulate(n, n, 300, 4000, seed=99)[50:]
    out(f"Standard deviation of the estimate, m/n = 1, n = {n}: {s.std():.2%}")
f2 = simulate(N_REAL, N_REAL, 15, 20000, seed=11)
lo, hi = np.percentile(f2[15], [5, 95])
out(f"Figure 2, version 15, m/n = 1: mean {f2[15].mean() * BP:.0f} bp, 5th-95th percentiles "
    f"{lo * BP:.0f}-{hi * BP:.0f} bp, expected path {fixed_point(1.0) * BP:.0f} bp")
# Lane (2000): spread = expected loss + 0.5551 PFL^0.4946 CEL^0.5741, with CEL = 1
lane = lambda p: p + 0.5551 * p ** 0.4946
for ps in (0.005, 0.01, 0.02):
    out(f"Spread under Lane (2000) pricing, p* = {ps:.1%}, m/n = 1: "
        f"{1 - lane(fixed_point(1.0, ps=ps)) / lane(ps):.1%} below the true spread")
for name, g in [("probabilities", lambda p: p), ("spreads, 2.7 x p", lambda p: 2.7 * p),
                ("spreads, Lane (2000)", lane)]:
    d0, d1 = [g(fixed_point(r, 0.02)) - g(fixed_point(r, 0.005)) for r in (0, 1)]
    out(f"Difference between the 2% and 0.5% issuers in {name}: {d0 * 1e4:.0f} -> {d1 * 1e4:.0f} bp "
        f"at m/n = 0 -> 1 ({1 - d1 / d0:.0%} smaller)")
out()

out("## Accuracy and the synthetic share (Sections 3 and 8, Proposition A.1)")
grid = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0]
rmse = [np.sqrt(np.mean((simulate(N_REAL, int(round(r * N_REAL)), 400, 4000,
                                  seed=int(100 * r) + 1)[100:] - PSTAR) ** 2)) for r in grid]
out("RMSE by m/n: " + ", ".join(f"{r:g}: {e:.3%}" for r, e in zip(grid, rmse)))
for r in [0, 1.0]:
    m = int(round(r * N_REAL))
    s = simulate(N_REAL, m, 400, 4000, seed=7)[100:]
    se = np.sqrt(s.mean() / (N_REAL + m))
    out(f"m/n = {r:g}: standard deviation of the estimate {s.std():.3%}, standard error the firm "
        f"perceives {se:.3%}, standard deviation of the change between versions "
        f"{np.diff(s, axis=0).std():.3%}")
out(f"Proposition A.1 holds for p* above {P0 * (2 / (1 + 2 * GAMMA)) ** (1 / (GAMMA - 1)):.3%}")
out()

out("## Costly real data (Sections 4, 6 and 7)")
n_hi, n_lo = OBS_PER_YEAR * WIN_H, OBS_PER_YEAR * WIN_L
for g in [GAMMA, 1.05, 1.20]:
    hg = partial(h_tail_index, gamma=g)
    out(f"gamma = {g}: two states for cutoffs between {fixed_point(M_SYN / n_lo, h=hg) * BP:.0f} and "
        f"{fixed_point(M_SYN / n_hi, h=hg) * BP:.0f} bp")
out(f"Cutoff {P_CUT * BP:.0f} bp")
ps = np.full(WIN_H + 76, PSTAR)
ps[WIN_H + 10:WIN_H + 30] = 0.005
est, kept = maintenance_path(ps, extra_events={WIN_H + 45: 9}, p_init=fixed_point(1.0))
stop = int(np.argmax(~kept))
out(f"20-year calm from year 10: maintenance stops in year {stop}; spread after the calm "
    f"{est[44] * BP:.0f} bp; restored after the cluster in year 45")
m_lo = brentq(lambda m: fixed_point(m / n_lo) - cutoff(m), 1, M_SYN)
m_hi = brentq(lambda m: fixed_point(m / n_hi) - cutoff(m), M_SYN, 10 * M_SYN)
out(f"Synthetic draws: two states for m between {m_lo:.0f} and {m_hi:.0f}")
m_t = np.full(WIN_H + 60, float(M_SYN))
m_t[WIN_H + 10:WIN_H + 15] = 3000
est, kept = maintenance_path(np.full(WIN_H + 60, PSTAR), m=m_t, pc=cutoff(m_t),
                             p_init=fixed_point(1.0))
out(f"m = 3,000 in years 10-14: maintenance stops in year {int(np.argmax(~kept))}; spread "
    f"{est[-1] * BP:.0f} bp after m returns to 2,000")
m = 1000
out(f"m = {m}: data-poor spread {fixed_point(m / n_lo) * BP:.0f} bp, cutoff {cutoff(m) * BP:.0f} bp")
out("Share of markets data-poor 40 years after a calm ends (after 60 years with no calm)")
for q, rho in [(1000, 0.0), (1000, 0.02), (1000, 0.005), (100, 0.0)]:
    res = []
    for L in [0, 10, 20]:
        path_ps = np.full(WIN_H + 20 + L + 40, PSTAR)
        path_ps[WIN_H + 20:WIN_H + 20 + L] = 0.005
        _, k = maintenance_simulate(path_ps, 4000, m=20 * q, q=q, rho=rho, seed=11 + L)
        res.append(np.mean(~k[-1]))
    out(f"{q} observations a year, rho = {rho}: no calm {res[0]:.2f}, 10-year calm {res[1]:.2f}, "
        f"20-year calm {res[2]:.2f}")
out()

out("## Size of losses (Section 9)")
ALPHA = 1.40    # Hill estimate of the tail index of the Danish losses (Section 5)
for g in [1.10, 1.25]:
    out(f"gamma = {g}: mean excess over any threshold above the reference level "
        f"{1 - (ALPHA - 1) / (g * ALPHA - 1):.0%} lower than in the data")

(OUT / "theory_results.md").write_text("\n".join(lines) + "\n")
