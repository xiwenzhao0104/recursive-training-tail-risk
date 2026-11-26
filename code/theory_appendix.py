"""Theoretical and numerical results for Appendix B and Table 4.

Writes output/results/appendix_b_theory.md. Runs in a few minutes.
"""
from functools import partial
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm, genpareto

from model import (PSTAR, BP, N_REAL, GAMMA, P0, WIN_H, WIN_L, P_CUT, M_SYN, OBS_PER_YEAR,
                   h_tail_index, fixed_point, maintenance_path, maintenance_simulate, cutoff,
                   delta)

OUT = Path(__file__).resolve().parents[1] / "output" / "results"
OUT.mkdir(parents=True, exist_ok=True)
lines = []
R3 = [0.5, 1.0, 2.0]
N_H, N_L = OBS_PER_YEAR * WIN_H, OBS_PER_YEAR * WIN_L


def out(s=""):
    print(s, flush=True)
    lines.append(s)


def pct(p, d=2):
    return f"{100 * p:.{d}f}"


def fp(r, ps=PSTAR, h=h_tail_index):
    return fixed_point(r, ps=ps, h=h)


def crossings(h, ps, r, lo=1e-8):
    """Number of fixed points of Phi in (0, P0), counted on a fine logarithmic grid."""
    g = np.logspace(np.log10(lo), np.log10(P0) - 1e-9, 200_000)
    w = 1 / (1 + r)
    f = w * ps + (1 - w) * h(g) - g
    return int(np.sum(np.sign(f[1:]) != np.sign(f[:-1])))


# Appendix B.1: alternative tail distributions
out("# Appendix B: theoretical robustness")
out()
out("## B.1 Alternative heavy-tailed distributions")
Z0 = norm.isf(P0)
Y0 = np.log(-np.log(P0))


def h_power(p, c):
    """Pareto tail with index c times the learned one, an exponential tail with scale divided by
    c, or the proportional-hazards transform of any distribution with parameter c."""
    return P0 * (np.asarray(p, float) / P0) ** c


def h_lognormal(p, c):
    """Lognormal model whose log-volatility is 1/c times the learned one, matched at x0."""
    return norm.sf(Z0 + c * (norm.isf(np.asarray(p, float)) - Z0))


def h_weibull(p, c):
    """Weibull model whose shape is c times the learned one, matched at x0."""
    p = np.asarray(p, float)
    return np.exp(-np.exp(Y0 + c * (np.log(-np.log(p)) - Y0)))


x_dk = np.loadtxt(Path(__file__).resolve().parents[1] / "data" / "danish.csv", delimiter=",",
                  skiprows=1, usecols=0)
X0 = np.quantile(x_dk, 1 - P0)
XI, _, SIG = genpareto.fit(x_dk[x_dk > X0] - X0, floc=0)


def h_gpd_for(ps):
    """GPD above x0 with the Danish scale; the model learns the shape xi from its estimate at the
    issuer's threshold and generates with shape xi / c."""
    d = SIG / XI * ((ps / P0) ** (-XI) - 1)

    def h(p, c):
        p = np.atleast_1d(np.asarray(p, float))
        res = np.empty_like(p)
        for i, q in enumerate(p):
            if q >= P0:
                res[i] = q
                continue
            k = brentq(lambda k: P0 * (1 + k * d / SIG) ** (-1 / k) - q, 1e-6, 50)
            km = k / c
            res[i] = P0 * (1 + km * d / SIG) ** (-1 / km)
        return res if res.size > 1 else float(res[0])
    return h


FAMILIES = [("Pareto (baseline)", lambda ps: h_power), ("Lognormal", lambda ps: h_lognormal),
            ("Weibull", lambda ps: h_weibull), ("Generalized Pareto", h_gpd_for)]
out(f"GPD fitted to Danish losses above the 90th percentile: shape {XI:.2f} (tail index "
    f"{1 / XI:.2f}), scale {SIG:.2f}")
target = float(h_power(PSTAR, GAMMA))
out(f"Baseline one-round sampling rate at 1%: {pct(target, 3)}%")
out("family | c | h(1%) | estimate at m/n = 0.5, 1, 2 | relative bias at m/n=1 for p* = 0.5%, 1%, 2%"
    " | max number of fixed points")
for name, fac in FAMILIES:
    h1 = fac(PSTAR)
    c_match = brentq(lambda c: float(h1(PSTAR, c)) - target, 1.0001, 5)
    for lab, c in [("c = 1.1", GAMMA), ("matched", c_match)]:
        ests = [fp(r, h=lambda p, c=c: h1(p, c)) for r in R3]
        rel = []
        for ps in (0.005, 0.01, 0.02):
            hh = fac(ps)
            rel.append(1 - fp(1.0, ps=ps, h=lambda p, c=c, hh=hh: hh(p, c)) / ps)
        nx = 0 if name == "Generalized Pareto" else max(
            crossings(lambda g, c=c: h1(g, c), ps, r) for ps in (0.001, 0.01, 0.05, 0.09)
            for r in (0.1, 1, 10, 100))
        out(f"{name} | {lab} ({c:.3f}) | {pct(float(h1(PSTAR, c)), 3)} | "
            + ", ".join(pct(e) for e in ests) + " | " + ", ".join(f"{100 * d:.1f}" for d in rel)
            + f" | {nx if nx else 'n.c.'}")
out()

# Uniqueness for any p* < p0 when h is increasing and convex
out("## B.2 Uniqueness and stability")
mx = 0
for g in (1.01, 1.1, 1.25, 1.5, 2.0, 3.0):
    for ps in (1e-4, 1e-3, 5e-3, 0.01, 0.03, 0.039, 0.05, 0.08, 0.099):
        for r in (0.1, 0.5, 1, 2, 5, 10, 50, 200):
            mx = max(mx, crossings(partial(h_tail_index, gamma=g), ps, r))
out(f"Lemma 1, gamma 1.01-3, p* 0.01%-9.9% (including above p-hat = {P0 * GAMMA ** (-1 / (GAMMA - 1)):.2%}),"
    f" m/n 0.1-200: largest number of fixed points {mx}")
for g in (1.05, 1.1, 1.5):
    gg = np.logspace(-7, np.log10(P0) - 1e-6, 20000)
    for nm, hf in [("lognormal", h_lognormal), ("Weibull", h_weibull)]:
        s = np.diff(hf(gg, g)) / np.diff(gg)
        if not np.all(np.diff(s) > -1e-12):
            out(f"   {nm}, c = {g}: h not convex")
out("h is increasing and convex for the Pareto, lognormal and Weibull forms (checked numerically)")

# Appendix B.3: a model that stops generating tail events when its estimate falls below p_f
out()
out("S-shaped h: Lemma 1 times a logistic cut-off at p_f with width s (no tail events once the "
    "estimate is well below p_f)")


def h_cut(p, pf, s=0.0002, g=GAMMA):
    p = np.asarray(p, float)
    return h_tail_index(p, gamma=g) / (1 + np.exp(-(p - pf) / s))


def all_fixed_points(h, ps, r):
    g = np.linspace(1e-6, P0 - 1e-9, 400_000)
    w = 1 / (1 + r)
    f = w * ps + (1 - w) * h(g) - g
    idx = np.where(np.sign(f[1:]) != np.sign(f[:-1]))[0]
    pts = []
    for i in idx:
        x = brentq(lambda q: w * ps + (1 - w) * float(h(q)) - q, g[i], g[i + 1])
        dphi = (1 - w) * (float(h(x + 1e-9)) - float(h(x - 1e-9))) / 2e-9
        pts.append((x, "stable" if dphi < 1 else "unstable"))
    return pts


for pf in (0.006, 0.007):
    for r in (0.5, 1.0, 2.0):
        pts = all_fixed_points(partial(h_cut, pf=pf), PSTAR, r)
        out(f"p_f = {pf:.1%}, m/n = {r}: " + "; ".join(f"{pct(x)}% ({s})" for x, s in pts)
            + f" | collapsed level p*/(1+m/n) = {pct(PSTAR / (1 + r))}%")
out()

# Appendix B.2: sensitivity to gamma and to the form of the gap
out("## B.3 Sensitivity to gamma and to the form of the tail-index gap")
out("gamma | relative bias at m/n = 0.5, 1, 2 (exact) | first-order approximation")
for g in (1.02, 1.05, 1.10, 1.15, 1.20, 1.25, 1.50):
    hg = partial(h_tail_index, gamma=g)
    ex = [1 - fp(r, h=hg) / PSTAR for r in R3]
    ap = [r * (g - 1) * np.log(P0 / PSTAR) / (1 + r * (g - 1) * np.log(P0 / PSTAR)) for r in R3]
    out(f"{g:.2f} | " + ", ".join(f"{100 * e:.1f}" for e in ex) + " | "
        + ", ".join(f"{100 * a:.1f}" for a in ap))
ALPHA = 1.40
kappa = (GAMMA - 1) * ALPHA
out(f"Additive gap: model tail index = learned index + kappa, kappa = {kappa:.2f} "
    f"(same h(1%) as gamma = 1.1 when the learned index is {ALPHA})")
for ps in (0.005, 0.01, 0.02):
    theta = (ps / P0) ** (kappa / ALPHA)          # u/x0 = (p*/p0)^(-1/alpha) at the data index
    out(f"   p* = {ps:.1%}: one-round ratio {theta:.3f}; relative bias at m/n = 0.5, 1, 2: "
        + ", ".join(f"{100 * (1 - 1 / (1 + r * (1 - theta))):.1f}" for r in R3)
        + " | multiplicative: " + ", ".join(f"{100 * (1 - fp(r, ps) / ps):.1f}" for r in R3))
out()

# Appendix B.4: weights on synthetic draws
out("## B.4 Weights on synthetic draws")
out("weight | estimate at m/n = 0.5, 1, 2 | Section 4 calibration: data-rich, data-poor, cutoff "
    "(bp), states | spread 40 years after a 20-year calm (bp)")
for lam in (1.0, 0.75, 0.5, 0.25, 0.0):
    ests = [fp(lam * r) for r in R3]
    me = lam * M_SYN
    pH, pL = fp(me / N_H), fp(me / N_L)
    pc = cutoff(me) if me > 0 else cutoff(1e-9)
    states = ("both" if pL < pc <= pH else "data-rich only" if pc <= pL else "data-poor only")
    ps_path = np.full(WIN_H + 70, PSTAR)
    ps_path[WIN_H + 10:WIN_H + 30] = 0.005
    est, kept = maintenance_path(ps_path, m=me, pc=pc, p_init=pH)
    out(f"{lam:.2f} | " + ", ".join(pct(e) for e in ests)
        + f" | {pH * BP:.0f}, {pL * BP:.0f}, {pc * BP:.0f}, {states} | {est[-1] * BP:.0f}")
out()

# Appendix B.5: dependence and changing exposure
out("## B.5 Dependence over time and changing exposure (m/n = 1, n = 2,000 on average)")


def simulate_general(ps_years, q_years, R, rho=0.0, seed=0, window=WIN_H, ratio=1.0):
    """Binomial recursion with year-specific true probabilities and numbers of observations.
    ps_years has shape (T_total, R) and q_years shape (T_total,). The synthetic draws are
    ratio times the real draws in each version. Returns estimates (T_total - window, R) and the
    real frequency in each window."""
    rng = np.random.default_rng(seed)
    T = len(q_years)
    ev = np.empty((T, R))
    for t in range(T):
        if rho > 0:
            pt = ps_years[t]
            ev[t] = rng.binomial(q_years[t], rng.beta(pt * (1 - rho) / rho,
                                                      (1 - pt) * (1 - rho) / rho))
        else:
            ev[t] = rng.binomial(q_years[t], ps_years[t])
    cs = np.vstack([np.zeros(R), np.cumsum(ev, axis=0)])
    cq = np.concatenate([[0], np.cumsum(q_years)])
    p = np.full(R, PSTAR)
    est, freq = [], []
    for t in range(window, T):
        kr = cs[t] - cs[t - window]
        n = cq[t] - cq[t - window]
        m = int(round(ratio * n))
        ks = rng.binomial(m, np.clip(h_tail_index(p), 0, 1))
        p = (kr + ks) / (n + m)
        est.append(p)
        freq.append(kr / n)
    return np.array(est), np.array(freq)


TT, RR, BURN = 320, 3000, 60
rng = np.random.default_rng(5)
cases = []
q_flat = np.full(TT, OBS_PER_YEAR)
cases.append(("Independent draws (baseline)", np.full((TT, RR), PSTAR), q_flat, 0.0))
for rho_ar, sd in [(0.5, 0.5), (0.9, 0.5)]:
    z = np.zeros((TT, RR))
    eps = rng.standard_normal((TT, RR))
    for t in range(1, TT):
        z[t] = rho_ar * z[t - 1] + np.sqrt(1 - rho_ar ** 2) * sd * eps[t]
    pr = np.exp(z)
    pr = PSTAR * pr / pr.mean()
    cases.append((f"Log probability AR(1), persistence {rho_ar}, s.d. {sd}", pr, q_flat, 0.0))
st = np.zeros((TT, RR), dtype=int)
u = rng.random((TT, RR))
for t in range(1, TT):
    st[t] = np.where(u[t] < 0.1, 1 - st[t - 1], st[t - 1])
cases.append(("Two regimes, 0.5% and 1.5%, switching with prob. 0.1 a year",
              np.where(st == 1, 0.015, 0.005), q_flat, 0.0))
g_exp = 1.03 ** np.arange(TT)
cases.append(("Exposure growing 3% a year", np.full((TT, RR), PSTAR),
              np.maximum(1, np.round(OBS_PER_YEAR * g_exp / g_exp[-WIN_H:].mean() * 1.0)).astype(int),
              0.0))
cases.append(("Clustering within years, intra-class correlation 0.05",
              np.full((TT, RR), PSTAR), q_flat, 0.05))
cases.append(("Clustering within years, intra-class correlation 0.10",
              np.full((TT, RR), PSTAR), q_flat, 0.10))
out("case | mean real frequency in window | mean estimate | estimate / real frequency | "
    "deterministic fixed point / p* | s.d. of estimate")
for i, (name, pr, q, rho) in enumerate(cases):
    if name.startswith("Exposure"):
        # exposure path: evaluate the last 60 versions only (exposure keeps growing)
        est, freq = simulate_general(pr, q, RR, rho=rho, seed=100 + i)
        est, freq = est[-60:], freq[-60:]
    else:
        est, freq = simulate_general(pr, q, RR, rho=rho, seed=100 + i)
        est, freq = est[BURN:], freq[BURN:]
    out(f"{name} | {pct(freq.mean(), 3)} | {pct(est.mean(), 3)} | {est.mean() / freq.mean():.3f} | "
        f"{fp(1.0) / PSTAR:.3f} | {pct(est.std(), 3)}")
out()

# Appendix B.6: continuous choice of history
out("## B.6 Continuous choice of the length of history")
out("The firm chooses T in [T_L, T_H] each year to minimize L p/(qT+m) + c(T).")


def T_star(p, k):
    """Optimal history for perceived loss L p/(qT+m) with linear cost c(T) = k L T. k is the cost
    relative to L."""
    T = (np.sqrt(p * OBS_PER_YEAR / k) - M_SYN) / OBS_PER_YEAR
    return float(np.clip(T, WIN_L, WIN_H))


def Phi_cont(p, k, ps=PSTAR):
    n = OBS_PER_YEAR * T_star(p, k)
    return (n * ps + M_SYN * float(h_tail_index(p))) / (n + M_SYN)


def cont_fixed_points(k, ps=PSTAR):
    g = np.linspace(2e-4, 0.0101, 4000)
    f = np.array([Phi_cont(x, k, ps) - x for x in g])
    idx = np.where(np.sign(f[1:]) != np.sign(f[:-1]))[0]
    pts = []
    for i in idx:
        x = brentq(lambda q: Phi_cont(q, k, ps) - q, g[i], g[i + 1])
        d = (Phi_cont(x + 1e-7, k, ps) - Phi_cont(x - 1e-7, k, ps)) / 2e-7
        pts.append((x, "stable" if d < 1 else "unstable", T_star(x, k)))
    return pts


pH = fp(M_SYN / N_H)
# k at which the firm chooses T_H years at the data-rich estimate (scale 1), and multiples of it
k0 = pH * OBS_PER_YEAR / (N_H + M_SYN) ** 2
out("linear cost:")
for mult in (0.6, 1.0, 1.5, 2.0, 3.0):
    pts = cont_fixed_points(k0 * mult)
    out(f"   cost x {mult}: " + "; ".join(f"{x * BP:.0f} bp ({s}, T = {T:.1f} yrs)"
                                         for x, s, T in pts))
two = [mult for mult in np.arange(0.5, 3.0001, 0.01)
       if sum(s == "stable" for _, s, _ in cont_fixed_points(k0 * mult)) == 2]
out(f"   two stable states for cost multiples {min(two):.2f}-{max(two):.2f}"
    if two else "   never two stable states for cost multiples 0.5-3")
# calm experiment with the cost at which T_H is chosen at the data-rich estimate
ps_years = np.full(WIN_H + 90, PSTAR)
ps_years[WIN_H + 10:WIN_H + 30] = 0.005
p, ev, traj = pH, OBS_PER_YEAR * ps_years, []
for t in range(WIN_H, len(ps_years)):
    T = T_star(p, k0)
    Ti = int(np.floor(T))
    frac = T - Ti
    kr = ev[t - Ti + 1:t + 1].sum() + frac * ev[t - Ti]
    p = (kr + M_SYN * float(h_tail_index(p))) / (OBS_PER_YEAR * T + M_SYN)
    traj.append((p, T))
traj = np.array(traj)
out(f"   20-year calm (cost x 1): history falls to {traj[:40, 1].min():.1f} years; spread 40 "
    f"years after the calm {traj[69, 0] * BP:.0f} bp (history {traj[69, 1]:.1f} years)")
out()

# Appendix B.6: other objectives
out("## B.7 Other objectives")
pL = fp(M_SYN / N_L)
for kexp in (1.0, 2.0, 4.0):
    out(f"Loss L|e|^{kexp:g}: perceived value of the history is proportional to p^{kexp / 2:g}, "
        "so the cutoff rule holds")
# Informed firm: value of the history includes the reduction in squared bias
FL = P_CUT * delta(M_SYN)          # F / L in the baseline


def informed_value(p_hat):
    """Value of keeping the history for a firm that knows gamma: reduction in the mean-squared
    error of the long-run estimate, evaluated at the true probability implied by p_hat."""
    vals = []
    for n in (N_L, N_H):
        r = M_SYN / n
        ps_impl = p_hat * (1 + r * (1 - float(h_tail_index(p_hat)) / p_hat))
        b = ps_impl - p_hat
        vals.append(b ** 2 + p_hat / (n + M_SYN))
    return vals[0] - vals[1]


pc_inf = brentq(lambda p: informed_value(p) - FL, 1e-6, 0.05)
out(f"Naive firm cutoff {P_CUT * BP:.0f} bp; firm that knows gamma: cutoff {pc_inf * BP:.0f} bp "
    f"(data-poor estimate {pL * BP:.0f} bp, data-rich {pH * BP:.0f} bp)")
lo, hi = pL * delta(M_SYN), pH * delta(M_SYN)
out(f"Two states exist for F/L between {lo:.2e} and {hi:.2e}, a factor of {hi / lo:.1f}; "
    f"baseline F/L {FL:.2e}")
out()

# Appendix B.7: pricing functions
out("## B.8 Pricing functions (p* = 1%, m/n = 1)")
pbar = fp(1.0)
lam_w = norm.ppf(2.7 * PSTAR) - norm.ppf(PSTAR)
k_sd = (2.7 * PSTAR - PSTAR) / np.sqrt(PSTAR * (1 - PSTAR))
PRICING = [
    ("Constant multiple 2.7 (baseline)", lambda p: 2.7 * p),
    ("Multiple 2.0 (soft market)", lambda p: 2.0 * p),
    ("Multiple 4.0 (hard market)", lambda p: 4.0 * p),
    ("Lane (2000)", lambda p: p + 0.5551 * p ** 0.4946),
    ("2.7 x p plus 100 bp for liquidity and maturity", lambda p: 0.01 + 2.7 * p),
    (f"Wang transform, lambda = {lam_w:.2f}", lambda p: norm.cdf(norm.ppf(p) + lam_w)),
    (f"Expected loss plus {k_sd:.3f} s.d.", lambda p: p + k_sd * np.sqrt(p * (1 - p))),
    ("Three-year bond, 2.7 x annualized probability",
     lambda p: 2.7 * (1 - (1 - p) ** 3) / 3),
]
out("pricing | true spread (bp) | long-run spread (bp) | bias (bp) | bias (% of true spread) | "
    "bias for p* = 0.5% and 2% (%)")
for name, s in PRICING:
    t, e = s(PSTAR), s(pbar)
    o = [1 - s(fp(1.0, ps)) / s(ps) for ps in (0.005, 0.02)]
    out(f"{name} | {t * 1e4:.0f} | {e * 1e4:.0f} | {(t - e) * 1e4:.0f} | {100 * (1 - e / t):.1f} | "
        + ", ".join(f"{100 * x:.1f}" for x in o))
out()

# Appendix B.7: minimum share of real data
out("## B.9 Minimum share of real data for a tolerated relative bias")
out("The rule uses only the model's own estimate p and gamma, p0: "
    "m/n <= delta / ((1 - delta)(1 - theta(p)))")
out("gamma | estimate | max m/n (min real share) for tolerated bias 5% | 10% | 20%")
for g in (1.05, 1.10, 1.25):
    for p in (0.005, 0.01, 0.02):
        th = (p / P0) ** (g - 1)
        cells = []
        for d in (0.05, 0.10, 0.20):
            rmax = d / ((1 - d) * (1 - th))
            cells.append(f"{rmax:.2f} ({100 / (1 + rmax):.0f}%)")
        out(f"{g:.2f} | {p:.1%} | " + " | ".join(cells))
out()

# Table 4: policies under different market conditions
out("## B.10 Policies under different market conditions (Section 4 calibration)")


def scenario(m=M_SYN, g=GAMMA, n_rule=None, calm=True, lam=1.0):
    hg = partial(h_tail_index, gamma=g)
    me = lam * m
    pc = cutoff(me)
    ps_years = np.full(WIN_H + 70, PSTAR)
    if calm:
        ps_years[WIN_H + 10:WIN_H + 30] = 0.005
    if n_rule is not None:
        # fixed window of n_rule observations, no maintenance choice
        w = n_rule // OBS_PER_YEAR
        est, _ = maintenance_path(ps_years, m=me, pc=0.0, win_h=w, win_l=w, h=hg,
                                  p_init=fixed_point(me / n_rule, h=hg))
        return est[-1], fixed_point(me / n_rule, h=hg)
    p_rich = fixed_point(me / N_H, h=hg)
    p_init = p_rich if p_rich >= pc else fixed_point(me / N_L, h=hg)
    est, _ = maintenance_path(ps_years, m=me, pc=pc, h=hg, p_init=p_init)
    steady = p_init
    return est[-1], steady


POLICIES = [("No policy", {}), ("Minimum real share (20-year history)", {"n_rule": N_H}),
            ("Tail validation (gamma = 1.02)", {"g": 1.02}),
            ("Synthetic draws weighted 0.5", {"lam": 0.5}),
            ("Subsidy (m from 2,000 to 3,000)", {"m": 3000}),
            ("Recent-data rule (last 5 years)", {"n_rule": 500})]
out("policy | gamma = 1.1: steady state, after a 20-year calm | gamma = 1.25: steady state, after a"
    " 20-year calm (long-run spread in bp; true spread 270)")
for name, kw in POLICIES:
    cells = []
    for g in (GAMMA, 1.25):
        kk = dict(kw)
        if "g" not in kk:
            kk["g"] = g
        after, steady = scenario(**kk)
        cells.append(f"{steady * BP:.0f}, {after * BP:.0f}")
    out(f"{name} | " + " | ".join(cells))
out("Stochastic version, 1,000 observations a year: share of markets data-poor 40 years after a "
    "20-year calm")
for name, kw in POLICIES:
    if "n_rule" in kw:
        out(f"   {name}: no maintenance choice")
        continue
    m = kw.get("m", M_SYN) * 10 * kw.get("lam", 1.0)
    g = kw.get("g", GAMMA)
    pc = cutoff(m / 10)
    path_ps = np.full(WIN_H + 20 + 20 + 40, PSTAR)
    path_ps[WIN_H + 20:WIN_H + 40] = 0.005
    _, k = maintenance_simulate(path_ps, 2000, m=int(m), pc=pc, q=1000,
                                h=partial(h_tail_index, gamma=g), seed=7)
    out(f"   {name}: {np.mean(~k[-1]):.2f}")

(OUT / "appendix_b_theory.md").write_text("\n".join(lines) + "\n")
