"""Data, thresholds, tail measures, textbook models and the recursion used in Section 5.

Thresholds come from the real losses: the reference level x0 is the 90th percentile
(p0 = 10%), and tail events are losses above the 99th, 99.5th and 99.8th percentiles.
"""
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "danish.csv"
RES = ROOT / "output" / "results"
FIG = ROOT / "output" / "figures"
RES.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
torch.set_num_threads(4)

x_real = np.loadtxt(DATA, delimiter=",", skiprows=1, usecols=0)
N_REAL = len(x_real)
P0 = 0.10
PS = [0.01, 0.005, 0.002]
X0 = float(np.quantile(x_real, 1 - P0))
U = {p: float(np.quantile(x_real, 1 - p)) for p in PS}
N_SYN = 400_000          # synthetic draws per model


class Log:
    """Prints lines and saves them to output/results/<name>.md."""

    def __init__(self, name):
        self.path, self.lines = RES / f"{name}.md", []

    def __call__(self, s=""):
        print(s, flush=True)
        self.lines.append(s)

    def save(self):
        self.path.write_text("\n".join(self.lines) + "\n")


def hill(x, frac):
    """Hill estimate of the tail index from the largest frac share of x."""
    xs = np.sort(x)[::-1]
    k = max(int(frac * len(xs)), 10)
    return 1.0 / np.mean(np.log(xs[:k] / xs[k]))


def tail_stats(xs):
    """Exceedance frequencies, the implied gamma ln(h/p0)/ln(p/p0) and Hill indices."""
    d = {"ref": float(np.mean(xs > X0)), "max": float(xs.max())}
    for p in PS:
        h = float(np.mean(xs > U[p]))
        d[f"h{p}"] = h
        d[f"gamma{p}"] = float(np.log(h / P0) / np.log(p / P0)) if h > 0 else float("inf")
    pos = xs[xs > 0]
    d["hill10"] = float(hill(pos, 0.10))
    d["hill05"] = float(hill(pos, 0.05))
    return d


def median_stats(stats):
    return {k: float(np.median([s[k] for s in stats])) for k in stats[0]}


real = tail_stats(x_real)


class Transform:
    """Standardizes losses on the log scale."""

    def __init__(self, x):
        y = np.log(x)
        self.mu, self.sd = y.mean(), y.std()

    def fwd(self, x):
        return (np.log(x) - self.mu) / self.sd

    def inv(self, z):
        return np.exp(z * self.sd + self.mu)


def mlp(i, o, h=64, act=None):
    act = act if act is not None else nn.LeakyReLU(0.2)
    return nn.Sequential(nn.Linear(i, h), act, nn.Linear(h, h), act, nn.Linear(h, o))


def fit_gan(y, seed, steps=4000, zdim=4, hidden=64):
    """Standard (non-saturating) GAN driven by normal noise."""
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    G, D = mlp(zdim, 1, hidden), mlp(1, 1, hidden)
    og = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
    od = torch.optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))
    Y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
    bs = 256
    for _ in range(steps):
        real_b = Y[torch.tensor(rng.integers(0, len(Y), bs))]
        fake = G(torch.randn(bs, zdim)).detach()
        loss_d = F.softplus(-D(real_b)).mean() + F.softplus(D(fake)).mean()
        od.zero_grad(); loss_d.backward(); od.step()
        loss_g = F.softplus(-D(G(torch.randn(bs, zdim)))).mean()
        og.zero_grad(); loss_g.backward(); og.step()

    def sample(n):
        with torch.no_grad():
            return G(torch.randn(n, zdim)).squeeze(1).numpy()
    return sample


def fit_vae(y, seed, steps=4000, zdim=2, hidden=64):
    """Variational autoencoder with a normal prior and a Gaussian likelihood."""
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    enc = mlp(1, 2 * zdim, hidden, nn.ReLU())
    dec = mlp(zdim, 1, hidden, nn.ReLU())
    logs2 = nn.Parameter(torch.tensor(-2.0))
    opt = torch.optim.Adam(list(enc.parameters()) + list(dec.parameters()) + [logs2], lr=1e-3)
    Y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
    bs = 256
    for _ in range(steps):
        yb = Y[torch.tensor(rng.integers(0, len(Y), bs))]
        h = enc(yb)
        mu, lv = h[:, :zdim], h[:, zdim:]
        z = mu + torch.exp(0.5 * lv) * torch.randn_like(mu)
        nll = 0.5 * (((yb - dec(z)) ** 2) / torch.exp(logs2) + logs2).sum(1).mean()
        kl = -0.5 * (1 + lv - mu ** 2 - torch.exp(lv)).sum(1).mean()
        opt.zero_grad(); (nll + kl).backward(); opt.step()

    def sample(n):
        with torch.no_grad():
            m = dec(torch.randn(n, zdim)).squeeze(1)
            return (m + torch.exp(0.5 * logs2) * torch.randn(n)).numpy()
    return sample


def fit_gmm(y, seed, K=3, iters=300):
    """Gaussian mixture fitted by the EM algorithm."""
    rng = np.random.default_rng(seed)
    w, mu, sd = np.full(K, 1 / K), rng.choice(y, K, replace=False), np.full(K, y.std())
    for _ in range(iters):
        dens = w * np.exp(-0.5 * ((y[:, None] - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
        r = dens / dens.sum(1, keepdims=True)
        nk = r.sum(0) + 1e-12
        w = nk / len(y)
        mu = (r * y[:, None]).sum(0) / nk
        sd = np.sqrt((r * (y[:, None] - mu) ** 2).sum(0) / nk) + 1e-6

    def sample(n):
        g = np.random.default_rng(seed + 1)
        c = g.choice(K, n, p=w)
        return mu[c] + sd[c] * g.standard_normal(n)
    return sample


TEXTBOOK = {"GAN": fit_gan, "VAE": fit_vae, "Gaussian mixture": fit_gmm}


def textbook_sample(name, x_train, seed, n=N_SYN, **kw):
    tr = Transform(x_train)
    return tr.inv(TEXTBOOK[name](tr.fwd(x_train), seed, **kw)(n))


def recursion(sample_fn, seed, gens, ratio=1.0):
    """Trains generation 0 on the real losses and each later generation on the real losses plus
    ratio x N_REAL synthetic losses from the previous one. Returns, by generation, the share of
    training losses above the real 1% threshold (the estimate) and the share of the model's own
    synthetic losses above it (h)."""
    u1 = U[0.01]
    g_rng = np.random.default_rng(seed)
    xs = sample_fn(x_real, seed)
    est, hs = [float(np.mean(x_real > u1))], [float(np.mean(xs > u1))]
    for g in range(1, gens + 1):
        syn = xs[g_rng.integers(0, len(xs), int(ratio * N_REAL))]
        train = np.concatenate([x_real, syn])
        est.append(float(np.mean(train > u1)))
        xs = sample_fn(train, seed * 100 + g)
        hs.append(float(np.mean(xs > u1)))
    return {"estimate": est, "h": hs}
