"""Section 5: CTGAN, TVAE and the Gaussian copula from SDV, with SDV's default settings unless
stated. Optional arguments one, other, rec and rec1000 run single parts."""
import json
import random
import sys
import time
import warnings

import numpy as np
import pandas as pd
import torch

warnings.filterwarnings("ignore")
from sdv.metadata import Metadata                                            # noqa: E402
from sdv.single_table import (GaussianCopulaSynthesizer, CTGANSynthesizer,   # noqa: E402
                              TVAESynthesizer)

import common as C                                                           # noqa: E402

SYNTH = {"CTGAN": CTGANSynthesizer, "TVAE": TVAESynthesizer,
         "Gaussian copula": GaussianCopulaSynthesizer}
HEAD = "model | P(>x0) | h(1%) | h(0.5%) | h(0.2%) | implied gamma (1%) | Hill top 10% | max"


def seed_all(s):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)


def sdv_sample(name, x, seed, n=C.N_SYN, **kw):
    seed_all(seed)
    df = pd.DataFrame({"loss": x})
    md = Metadata.detect_from_dataframes({"losses": df})
    s = SYNTH[name](md, **kw)
    s.fit({"losses": df})
    seed_all(seed + 7)
    o = s.sample(n)
    o = o["losses"] if isinstance(o, dict) else o
    return o["loss"].to_numpy(dtype=float)


def row(name, d):
    return (f"{name} | {d['ref']:.3f} | {d['h0.01']:.4f} | {d['h0.005']:.4f} | "
            f"{d['h0.002']:.4f} | {d['gamma0.01']:.2f} | {d['hill10']:.2f} | {d['max']:.0f}")


def part_one():
    out = C.Log("sdv_one_round")
    out("# SDV synthesizers: one round of training (median over 5 seeds)")
    res = {}
    for label, kw in [("SDV defaults", {}),
                      ("no clipping to the observed range", {"enforce_min_max_values": False})]:
        out(f"## {label}")
        out(HEAD)
        for name in SYNTH:
            st = [C.tail_stats(sdv_sample(name, C.x_real, s, **kw)) for s in range(1, 6)]
            res[f"{name} | {label}"] = {"runs": st, "median": C.median_stats(st)}
            out(row(name, C.median_stats(st)))
    json.dump(res, open(C.RES / "sdv_one_round.json", "w"), indent=1)
    out.save()


def part_other():
    out = C.Log("sdv_other_settings")
    out("# SDV synthesizers: other settings (median over 3 seeds)")
    out(HEAD)
    res = {}
    for name, kw, lab, n in [
            ("CTGAN", {"epochs": 1000}, "CTGAN, 1,000 epochs", C.N_SYN),
            ("TVAE", {"epochs": 1000}, "TVAE, 1,000 epochs", C.N_SYN),
            # kernel marginals are slow to sample
            ("Gaussian copula", {"default_distribution": "gaussian_kde"}, "copula, kernel marginal",
             20_000)]:
        st = [C.tail_stats(sdv_sample(name, C.x_real, s, n=n, **kw)) for s in range(1, 4)]
        res[lab] = {"runs": st, "median": C.median_stats(st)}
        out(row(lab, C.median_stats(st)))
    json.dump(res, open(C.RES / "sdv_other_settings.json", "w"), indent=1)
    out.save()


def part_rec(gens=6, seeds=(31, 32)):
    out = C.Log("sdv_recursion")
    out(f"# Recursive training with SDV defaults (m/n = 1, {gens} generations, {len(seeds)} seeds)")
    rec = {}
    for name in SYNTH:
        def fn(x, s, name=name):
            return sdv_sample(name, x, s)
        paths = [C.recursion(fn, s, gens) for s in seeds]
        rec[name] = paths
        p = paths[0]["estimate"][0]
        theta = np.mean([q["h"][0] for q in paths]) / p
        longrun = np.mean([q["estimate"][-3:] for q in paths])
        out(f"{name}: one-round ratio {theta:.2f}, Proposition 1 fixed point "
            f"{100 * p / (2 - theta):.3f}%, simulated long run {100 * longrun:.3f}%")
        for s, q in zip(seeds, paths):
            out(f"   seed {s}: estimate " + " ".join(f"{e:.4f}" for e in q["estimate"]))
    json.dump(rec, open(C.RES / "sdv_recursion.json", "w"), indent=1)
    out.save()


def part_rec_long(gens=6, seeds=(41, 42, 43, 44)):
    """CTGAN recursion with 1,000 training epochs, as a check that the downward drift is not an
    artefact of the default 300 epochs."""
    out = C.Log("sdv_recursion_ctgan1000")
    out(f"# CTGAN recursion with 1,000 epochs (m/n = 1, {gens} generations, {len(seeds)} seeds)")

    t0 = time.time()

    def fn(x, s):
        xs = sdv_sample("CTGAN", x, s, epochs=1000)
        print(f"   fit {s} done after {time.time() - t0:.0f}s", flush=True)
        return xs
    paths = []
    for s in seeds:
        q = C.recursion(fn, s, gens)
        paths.append(q)
        out(f"   seed {s}: estimate " + " ".join(f"{e:.4f}" for e in q["estimate"])
            + " | h " + " ".join(f"{e:.4f}" for e in q["h"]))
    p = paths[0]["estimate"][0]
    theta = np.mean([q["h"][0] for q in paths]) / p
    longrun = np.mean([q["estimate"][-3:] for q in paths])
    out(f"CTGAN, 1,000 epochs: one-round ratio {theta:.2f}, Proposition 1 fixed point "
        f"{100 * p / (2 - theta):.3f}%, simulated long run {100 * longrun:.3f}%")
    json.dump(paths, open(C.RES / "sdv_recursion_ctgan1000.json", "w"), indent=1)
    out.save()


if __name__ == "__main__":
    t0 = time.time()
    parts = sys.argv[1:] or ["one", "other", "rec", "rec1000"]
    if "one" in parts:
        part_one()
    if "other" in parts:
        part_other()
    if "rec" in parts:
        part_rec()
    if "rec1000" in parts:
        part_rec_long()
    print(f"Total time {time.time() - t0:.0f}s")
