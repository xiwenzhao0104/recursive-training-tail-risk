"""Loss datasets, thresholds, tail measures and the recursion used in Section 5 and Appendix B.

Each dataset is a vector of positive losses. As in Section 5, the reference level x0 is the 90th
percentile of the real losses (p0 = 10%), and tail events are losses above the 99th, 99.5th and
99.8th percentiles. The Danish data reproduce `common.py` exactly.
"""
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RES = ROOT / "output" / "results"
RAW = ROOT / "output" / "runs" / "appendix_b"
SAMPLES = RAW / "samples"
for d in (RES, SAMPLES, RAW):
    d.mkdir(parents=True, exist_ok=True)

P0 = 0.10
PS = [0.01, 0.005, 0.002]
HILL_FRACS = [0.025, 0.05, 0.10, 0.15, 0.20]
SOA_SUBSAMPLE = 10_000      # random subsample of the 75,789 SOA claims, to keep training times similar

LABELS = {"danish": "Danish fire", "norwegian": "Norwegian fire", "soa": "SOA medical",
          "sp500": "S&P 500 daily losses"}


def load(name):
    if name == "danish":
        return np.loadtxt(DATA / "danish.csv", delimiter=",", skiprows=1, usecols=0)
    if name == "norwegian":
        return np.loadtxt(DATA / "norwegian_fire.csv", delimiter=",", skiprows=1, usecols=0)
    if name == "soa":
        x = np.loadtxt(DATA / "soa_medical.csv", delimiter=",", skiprows=1, usecols=0)
        return np.sort(np.random.default_rng(0).choice(x, SOA_SUBSAMPLE, replace=False))
    if name == "sp500":
        return np.loadtxt(DATA / "sp500_losses.csv", delimiter=",", skiprows=1, usecols=0,
                          dtype=float)
    raise ValueError(name)


def hill(x, frac):
    """Hill estimate of the tail index from the largest frac share of x."""
    xs = np.sort(x)[::-1]
    k = max(int(frac * len(xs)), 10)
    return 1.0 / np.mean(np.log(xs[:k] / xs[k]))


class Dataset:
    def __init__(self, name, x=None):
        self.name = name
        self.x = load(name) if x is None else np.asarray(x, dtype=float)
        self.n = len(self.x)
        self.x0 = float(np.quantile(self.x, 1 - P0))
        self.u = {p: float(np.quantile(self.x, 1 - p)) for p in PS}
        self.real = self.tail_stats(self.x)

    def tail_stats(self, xs):
        """Exceedance frequencies, implied gamma ln(h/p0)/ln(p/p0), Hill indices and maximum."""
        xs = np.asarray(xs, dtype=float)
        d = {"ref": float(np.mean(xs > self.x0)), "max": float(xs.max())}
        for p in PS:
            h = float(np.mean(xs > self.u[p]))
            d[f"h{p}"] = h
            d[f"gamma{p}"] = float(np.log(h / P0) / np.log(p / P0)) if h > 0 else float("inf")
        pos = xs[xs > 0]
        for f in HILL_FRACS:
            d[f"hill{f}"] = float(hill(pos, f))
        return d


def recursion(ds, sample_fn, seed, gens, ratio=1.0, x_real=None):
    """Generation 0 is trained on the real losses and each later generation on the real losses
    plus ratio x n synthetic losses from the previous one (as in common.recursion). Returns, by
    generation, the share of training losses above the 1% threshold of ds (the estimate) and the
    share of the model's own synthetic losses above it (h)."""
    x_real = ds.x if x_real is None else x_real
    n = len(x_real)
    u1 = ds.u[0.01]
    g_rng = np.random.default_rng(seed)
    xs = sample_fn(x_real, seed)
    est, hs = [float(np.mean(x_real > u1))], [float(np.mean(xs > u1))]
    for g in range(1, gens + 1):
        syn = xs[g_rng.integers(0, len(xs), int(ratio * n))]
        train = np.concatenate([x_real, syn])
        est.append(float(np.mean(train > u1)))
        xs = sample_fn(train, seed * 100 + g)
        hs.append(float(np.mean(xs > u1)))
    return {"estimate": est, "h": hs}
