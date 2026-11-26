"""Summarizes the runs of appendix_runs.py into output/results/appendix_b_evidence.md (Tables B7-B10 and
the numbers in Appendix B.8-B.12)."""
import json
from collections import defaultdict

import numpy as np
from scipy.stats import beta as beta_dist, t as t_dist

import datasets as D

lines = []


def out(s=""):
    print(s, flush=True)
    lines.append(s)


def load_all():
    res = []
    for f in sorted(D.RAW.glob("*.json")):
        res.append(json.loads(f.read_text()))
    return res


RES = load_all()
DS = {name: D.Dataset(name) for name in D.LABELS}
MODELS = ["CTGAN", "TVAE", "Gaussian copula", "GAN", "VAE", "Gaussian mixture"]
MULT = 2.7


def cp_interval(k, n, a=0.05):
    lo = beta_dist.ppf(a / 2, k, n - k + 1) if k > 0 else 0.0
    hi = beta_dist.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi


def fmt_g(g):
    return "--" if not np.isfinite(g) else f"{g:.2f}"


# One round of training, all datasets
one = defaultdict(list)
for r in RES:
    j = r["job"]
    if j["kind"] == "one":
        one[(j["ds"], j["model"])].append((j["seed"], r["stats"]))

out("# Appendix B: empirical results")
out()
out("## Appendix B.8: one round of training, by dataset (medians over seeds)")
out("Columns: share above 90th / 99th / 99.5th / 99.8th percentile (percent), implied gamma, "
    "s.d. across seeds of the share above the 99th percentile, share of seeds below the real "
    "frequency, Hill index (top 10%), largest loss relative to the largest real loss")
for ds_name, ds in DS.items():
    rl = ds.real
    k = int(round(rl["h0.01"] * ds.n))
    lo, hi = cp_interval(k, ds.n)
    out(f"### {D.LABELS[ds_name]} (n = {ds.n}; {k} real losses above the 99th percentile, 95% "
        f"interval for their frequency {100 * lo:.2f}-{100 * hi:.2f}%; Hill index "
        f"{rl['hill0.1']:.2f})")
    for m in MODELS:
        runs = [s for _, s in sorted(one.get((ds_name, m), []), key=lambda t: t[0])]
        if not runs:
            continue
        med = {key: float(np.median([s[key] for s in runs])) for key in runs[0]}
        h1 = np.array([s["h0.01"] for s in runs])
        below = np.mean(h1 < rl["h0.01"])
        out(f"{m} ({len(runs)} seeds) | {100 * med['ref']:.1f} | {100 * med['h0.01']:.2f} | "
            f"{100 * med['h0.005']:.2f} | {100 * med['h0.002']:.2f} | {fmt_g(med['gamma0.01'])} | "
            f"{100 * h1.std(ddof=1):.2f} | {below:.0%} | {med['hill0.1']:.2f} | "
            f"{med['max'] / rl['max']:.2f}")
    out()

# Danish data: variation across seeds for the SDV tools (Table B8)
out("## Table B8: variation across training runs, Danish data, 100 seeds")
out("model | mean share above 99th pct (%) | s.d. | 95% interval for the mean | min-max | "
    "implied gamma: median, interquartile range")
for m in ["CTGAN", "TVAE", "Gaussian copula"]:
    runs = [s for _, s in sorted(one.get(("danish", m), []), key=lambda t: t[0])]
    if not runs:
        continue
    h1 = np.array([s["h0.01"] for s in runs])
    g = np.array([s["gamma0.01"] for s in runs])
    se = h1.std(ddof=1) / np.sqrt(len(h1))
    q = t_dist.ppf(0.975, len(h1) - 1)
    gq = np.percentile(g, [25, 50, 75])
    out(f"{m} | {100 * h1.mean():.2f} | {100 * h1.std(ddof=1):.2f} | "
        f"{max(0.0, 100 * (h1.mean() - q * se)):.2f}-{100 * (h1.mean() + q * se):.2f} | "
        f"{100 * h1.min():.2f}-{100 * h1.max():.2f} | {fmt_g(gq[1])}, {fmt_g(gq[0])}-{fmt_g(gq[2])}")
out()

# Other settings on the Danish data
hyp = defaultdict(list)
for r in RES:
    j = r["job"]
    if j["kind"] == "hyper":
        hyp[j["label"]].append(r["stats"])
out("## Table B9: other settings, Danish data (medians over 5 seeds)")
out("setting | 90th | 99th | 99.5th | 99.8th (percent) | implied gamma | Hill top 10% | max loss")
order = ["CTGAN, 100 epochs", "CTGAN, 1,000 epochs", "CTGAN, 3,000 epochs", "CTGAN, batch size 100",
         "CTGAN, layers of 64", "CTGAN, layers of 512", "TVAE, 100 epochs",
         "TVAE, 1,000 epochs", "TVAE, 3,000 epochs", "TVAE, layers of 256",
         "Copula, normal marginal", "Copula, truncated normal marginal", "Copula, gamma marginal"]
for lab in order:
    runs = hyp.get(lab)
    if not runs:
        continue
    med = {key: float(np.median([s[key] for s in runs])) for key in runs[0]}
    out(f"{lab} ({len(runs)}) | {100 * med['ref']:.1f} | {100 * med['h0.01']:.2f} | "
        f"{100 * med['h0.005']:.2f} | {100 * med['h0.002']:.2f} | {fmt_g(med['gamma0.01'])} | "
        f"{med['hill0.1']:.2f} | {med['max']:.0f}")
out()

# Threshold choices for gamma and the Hill estimator
out("## Appendix B.10: implied gamma under other reference and tail levels, and Hill-based gamma (Danish)")
dk = DS["danish"]
xr = np.sort(dk.x)


def implied(xs_sorted, xr_sorted, p0, p):
    """Implied gamma ln(h/p0)/ln(p/p0), with the tail threshold set at the 1 - p quantile of the
    real losses xr_sorted (as in Section 5)."""
    u = np.quantile(xr_sorted, 1 - p)
    h = 1 - np.searchsorted(xs_sorted, u, side="right") / len(xs_sorted)
    return np.log(h / p0) / np.log(p / p0) if h > 0 else np.inf


out("Real Hill index by share of the sample used: " + ", ".join(
    f"{100 * f:g}%: {D.hill(dk.x, f):.2f}" for f in D.HILL_FRACS))
def hill_boot(f, reps=1000):
    """Same resamples as the interval in Section 5 (textbook_models.py)."""
    rng = np.random.default_rng(0)
    return [D.hill(rng.choice(dk.x, dk.n), f) for _ in range(reps)]


boot = {f: hill_boot(f) for f in D.HILL_FRACS}
# random stream for the bootstrap of the implied gamma below
rng = np.random.default_rng(0)
for _ in range(len(D.HILL_FRACS) * 500):
    rng.choice(dk.x, dk.n)
out("   90% bootstrap intervals: " + ", ".join(
    f"{100 * f:g}%: {np.percentile(b, 5):.2f}-{np.percentile(b, 95):.2f}" for f, b in boot.items()))
samples = defaultdict(list)
for m in ["CTGAN", "TVAE", "Gaussian copula"]:
    for s in range(1, 101):
        f = D.SAMPLES / f"one__danish__{m.replace(' ', '_')}__s{s}.npy"
        if f.exists():
            samples[m].append(np.sort(np.load(f).astype(float)))
out("model | gamma from frequencies, reference level / tail level: 90th/99th (baseline), "
    "95th/99th, 80th/99th, 90th/99.5th | gamma as ratio of Hill indices (top 5%, 10%, 20%) | "
    "90% bootstrap interval of the baseline gamma (thresholds resampled)")
for m, xs_list in samples.items():
    cells = []
    for p0, p in [(0.10, 0.01), (0.05, 0.01), (0.20, 0.01), (0.10, 0.005)]:
        cells.append(fmt_g(float(np.median([implied(xs, xr, p0, p) for xs in xs_list]))))
    hr = []
    for f in (0.05, 0.10, 0.20):
        hr.append(fmt_g(float(np.median([D.hill(xs[xs > 0], f) for xs in xs_list])) / D.hill(dk.x, f)))
    bt = []
    for _ in range(300):
        xb = np.sort(rng.choice(dk.x, dk.n))
        bt.append(np.median([implied(xs, xb, 0.10, 0.01) for xs in xs_list]))
    bt = np.array(bt)
    fin = bt[np.isfinite(bt)]
    bi = (f"{np.percentile(bt, 5):.2f}-{np.percentile(bt, 95):.2f}" if len(fin) == len(bt)
          else f"{len(fin)}/{len(bt)} finite")
    out(f"{m} | " + ", ".join(cells) + " | " + ", ".join(hr) + f" | {bi}")
out()

# Recursive training
rec = defaultdict(list)
for r in RES:
    j = r["job"]
    if j["kind"] == "rec":
        rec[(j["ds"], j["model"], j["ratio"], j.get("nsub"), j["gens"])].append(r)
out("## Table B10: recursive training, predicted and simulated long-run estimates")
out("dataset | model | m/n | real draws | seeds | generations | real frequency (%) | one-round "
    "ratio | predicted (%) | simulated, mean of last 3 generations (%) | s.e. across seeds | "
    "simulated / predicted")
cells = []
for key in sorted(rec, key=lambda k: (list(D.LABELS).index(k[0]), MODELS.index(k[1]), k[2],
                                      k[3] or 0)):
    ds_name, m, ratio, nsub, gens = key
    rs = rec[key]
    p_real = np.array([q["estimate"][0] for q in rs])
    theta = np.mean([q["h"][0] / q["estimate"][0] for q in rs])
    pred = np.mean(p_real) / (1 + ratio * (1 - theta))
    per_seed = np.array([np.mean(q["estimate"][-3:]) for q in rs])
    sim = per_seed.mean()
    se = per_seed.std(ddof=1) / np.sqrt(len(per_seed)) if len(per_seed) > 1 else np.nan
    cells.append((pred / np.mean(p_real), sim / np.mean(p_real), se / np.mean(p_real), key))
    out(f"{D.LABELS[ds_name]} | {m} | {ratio:g} | {nsub or DS[ds_name].n} | {len(rs)} | {gens} | "
        f"{100 * np.mean(p_real):.2f} | {theta:.2f} | {100 * pred:.2f} | {100 * sim:.2f} | "
        f"{100 * se:.2f} | {sim / pred:.2f}")
if cells:
    a = np.array([(c[0], c[1]) for c in cells])
    slope, icept = np.polyfit(a[:, 0], a[:, 1], 1)
    corr = np.corrcoef(a[:, 0], a[:, 1])[0, 1]
    out(f"Across {len(cells)} cells, simulated/real on predicted/real: slope {slope:.2f}, "
        f"intercept {icept:.2f}, correlation {corr:.2f}; mean absolute gap "
        f"{100 * np.mean(np.abs(a[:, 1] - a[:, 0])):.1f} percent of the real frequency; share of "
        f"cells with simulated below real frequency {np.mean(a[:, 1] < 1):.0%}")
    out("Path by generation (mean across seeds, percent), m/n = 1, full Danish data, 10 generations:")
    for m in ["CTGAN", "TVAE", "Gaussian copula"]:
        rs = rec.get(("danish", m, 1.0, None, 10), [])
        if rs:
            est = np.mean([q["estimate"] for q in rs], axis=0)
            out(f"   {m}: " + " ".join(f"{100 * e:.2f}" for e in est))
out()

# Spread bias implied by each dataset and model
import sys                                                                    # noqa: E402
from functools import partial                                                 # noqa: E402
sys.path.insert(0, str(D.ROOT / "code"))
from model import fixed_point, h_tail_index                                   # noqa: E402

out("## Table B7, last two columns, and Appendix B.12: long-run bias implied by each dataset (p* = 1%, p0 = 10%, spread 2.7 x p)")
out("dataset | model | implied gamma (median over seeds) | long-run estimate at m/n = 0.5, 1, 2 "
    "(%) | relative bias at m/n = 1 (%) | spread bias at m/n = 1 (bp, positive = understated) | rarest level: gamma implied at "
    "the 99.8th percentile and relative bias of a 0.2% probability at m/n = 1 (%)")


def rare(runs):
    g2 = float(np.median([s["gamma0.002"] for s in runs]))
    p2 = (fixed_point(1.0, ps=0.002, h=partial(h_tail_index, gamma=g2)) if np.isfinite(g2)
          else 0.002 / 2)
    return f"{fmt_g(g2)}, {100 * (1 - p2 / 0.002):.0f}"


for ds_name, ds in DS.items():
    for m in MODELS:
        runs = [s for _, s in one.get((ds_name, m), [])]
        if not runs:
            continue
        g = float(np.median([s["gamma0.01"] for s in runs]))
        if np.isfinite(g):
            est = [fixed_point(r, h=partial(h_tail_index, gamma=g)) for r in (0.5, 1, 2)]
        else:                       # no synthetic tail events: h = 0
            est = [0.01 / (1 + r) for r in (0.5, 1, 2)]
        out(f"{D.LABELS[ds_name]} | {m} | {fmt_g(g)} | " + ", ".join(f"{100 * e:.2f}" for e in est)
            + f" | {100 * (1 - est[1] / 0.01):.0f}"
            + f" | {(0.01 - est[1]) * MULT * 1e4:.0f}" + f" | {rare(runs)}")
out()

# Rarity gradient, pooled frequencies and tail shape
out()
out("## Table B7: ratio of synthetic to real frequency by threshold, pooled over seeds")
out("dataset | model | seeds | pooled h/p at 99th, 99.5th, 99.8th (90% interval over seeds, "
    "bootstrap) | share of seeds with h/p falling from 99th to 99.8th | max synthetic / max real "
    "(median) | Hill index synthetic / real (median, top 10%)")
grad_all = defaultdict(list)
for ds_name, ds in DS.items():
    rl = ds.real
    for m in MODELS:
        runs = [s for _, s in sorted(one.get((ds_name, m), []), key=lambda t: t[0])]
        if not runs:
            continue
        cells = []
        for p in D.PS:
            v = np.array([s[f"h{p}"] for s in runs]) / rl[f"h{p}"]
            b = [rng.choice(v, len(v)).mean() for _ in range(2000)]
            cells.append(f"{v.mean():.2f} ({np.percentile(b, 5):.2f}-{np.percentile(b, 95):.2f})")
        falls = np.mean([s["h0.002"] / rl["h0.002"] < s["h0.01"] / rl["h0.01"] for s in runs])
        grad_all[m].extend([s["h0.002"] / rl["h0.002"] < s["h0.01"] / rl["h0.01"] for s in runs])
        mx = np.median([s["max"] for s in runs]) / rl["max"]
        hl = np.median([s["hill0.1"] for s in runs]) / rl["hill0.1"]
        out(f"{D.LABELS[ds_name]} | {m} | {len(runs)} | " + " | ".join(cells)
            + f" | {falls:.0%} | {mx:.2f} | {hl:.2f}")
out("Share of all runs in which h/p is lower at the 99.8th than at the 99th percentile: "
    + ", ".join(f"{m} {np.mean(v):.0%} ({len(v)})" for m, v in grad_all.items()))

(D.RES / "appendix_b_evidence.md").write_text("\n".join(lines) + "\n")
