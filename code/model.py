"""Model of "Synthetic Data, Recursive Training, and the Pricing of Tail Risk".

Notation follows the paper: p* is the true tail probability, n and m are the numbers of real
and synthetic draws, r = m/n, and h(p) is the probability that a model whose estimate is p
generates a tail event.
"""
import numpy as np

PSTAR = 0.01        # true tail probability
GAMMA = 1.10        # ratio of the model's tail index to that of the data
P0 = 0.10           # reference rate
N_REAL = 2000       # real draws (Section 6)
MULT = 2.7          # spread as a multiple of the estimate (Lane and Mahul, 2008)
BP = MULT * 1e4     # converts a probability into basis points of spread

# Section 4
OBS_PER_YEAR = 100
WIN_H, WIN_L = 20, 2    # years of usable history with and without maintenance
M_SYN = 2000
P_CUT = 0.006


def h_tail_index(p, gamma=GAMMA, p0=P0):
    """Equation (2)."""
    p = np.asarray(p, dtype=float)
    return p0 * (np.maximum(p, 0.0) / p0) ** gamma


H = h_tail_index


def Phi(p, r, ps=PSTAR, h=H):
    """Equation (3)."""
    w = 1.0 / (1.0 + r)
    return w * ps + (1.0 - w) * h(p)


def fixed_point(r, ps=PSTAR, h=H, tol=1e-15, maxit=500_000):
    p = ps
    for _ in range(maxit):
        q = float(Phi(p, r, ps, h))
        if abs(q - p) < tol:
            return q
        p = q
    return p


def path(r, T, ps=PSTAR, h=H):
    out = [ps]
    for _ in range(T):
        out.append(float(Phi(out[-1], r, ps, h)))
    return np.array(out)


def simulate(n, m, T, R, ps=PSTAR, h=H, seed=0, rho=0.0, window=WIN_H):
    """Equation (1) with binomial draws, for R markets over T versions.

    Real draws come from a rolling window of `window` years with n / window observations a year.
    With rho > 0, tail events within a year are beta-binomial with intra-class correlation rho.
    Returns an array of shape (T + 1, R).
    """
    rng = np.random.default_rng(seed)
    q = n // window
    if rho > 0:
        a, b = ps * (1 - rho) / rho, (1 - ps) * (1 - rho) / rho
        ev = rng.binomial(q, rng.beta(a, b, (window + T, R)))
    else:
        ev = rng.binomial(q, ps, (window + T, R))
    csum = np.vstack([np.zeros(R), np.cumsum(ev, axis=0)])
    p = np.full(R, ps)
    out = np.empty((T + 1, R))
    out[0] = p
    for t in range(1, T + 1):
        kr = csum[window + t] - csum[t]
        ks = rng.binomial(m, np.clip(h(p), 0.0, 1.0)) if m > 0 else 0
        p = (kr + ks) / (q * window + m)
        out[t] = p
    return out


def detection_events(delta):
    """Equation (5): real tail events needed to detect a relative bias delta."""
    d = np.asarray(delta, dtype=float)
    return ((1.959964 * np.sqrt(1.0 - d) + 0.841621) / d) ** 2


def delta(m, n_hi=OBS_PER_YEAR * WIN_H, n_lo=OBS_PER_YEAR * WIN_L):
    """Delta in equation (6)."""
    return 1.0 / (n_lo + m) - 1.0 / (n_hi + m)


def cutoff(m, pc=P_CUT, m0=M_SYN):
    """Cutoff F / (L Delta) with F / L fixed so that the cutoff is pc when m = m0."""
    return pc * delta(m0) / delta(m)


def maintenance_path(ps_by_year, m=M_SYN, pc=P_CUT, q=OBS_PER_YEAR, win_h=WIN_H, win_l=WIN_L,
                     h=H, extra_events=None, p_init=None):
    """Expected path of the estimate in Section 4.

    The firm maintains its historical data in a given year if its previous estimate is at least
    pc, and then uses the last win_h years of observations instead of the last win_l.
    ps_by_year is the true probability by year; m and pc can also be given by year.
    extra_events maps years to additional tail events. Returns the estimate and whether data
    were maintained, from year win_h onwards.
    """
    ev = q * np.asarray(ps_by_year, dtype=float)
    for yr, k in (extra_events or {}).items():
        ev[yr] += k
    m = np.broadcast_to(np.asarray(m, dtype=float), ev.shape)
    pc = np.broadcast_to(np.asarray(pc, dtype=float), ev.shape)
    p = ps_by_year[win_h] if p_init is None else p_init
    est, kept = [], []
    for t in range(win_h, len(ev)):
        keep = p >= pc[t]
        win = win_h if keep else win_l
        p = (ev[t - win + 1:t + 1].sum() + m[t] * float(h(p))) / (q * win + m[t])
        est.append(p)
        kept.append(keep)
    return np.array(est), np.array(kept)


def maintenance_simulate(ps_by_year, R, m=M_SYN, pc=P_CUT, q=OBS_PER_YEAR, win_h=WIN_H,
                         win_l=WIN_L, h=H, rho=0.0, seed=0):
    """Stochastic version of maintenance_path for R markets. With rho > 0, tail events cluster
    within years."""
    rng = np.random.default_rng(seed)
    ps_by_year = np.asarray(ps_by_year, dtype=float)
    T = len(ps_by_year)
    ev = np.empty((T, R))
    for t in range(T):
        if rho > 0:
            a = ps_by_year[t] * (1 - rho) / rho
            b = (1 - ps_by_year[t]) * (1 - rho) / rho
            ev[t] = rng.binomial(q, rng.beta(a, b, R))
        else:
            ev[t] = rng.binomial(q, ps_by_year[t], R)
    csum = np.vstack([np.zeros(R), np.cumsum(ev, axis=0)])
    p = np.full(R, ps_by_year[win_h])
    est, kept = [], []
    for t in range(win_h, T):
        keep = p >= pc
        win = np.where(keep, win_h, win_l)
        k_real = csum[t + 1] - csum[t + 1 - win, np.arange(R)]
        ks = rng.binomial(m, np.clip(h(p), 0.0, 1.0))
        p = (k_real + ks) / (q * win + m)
        est.append(p.copy())
        kept.append(keep.copy())
    return np.array(est), np.array(kept)
