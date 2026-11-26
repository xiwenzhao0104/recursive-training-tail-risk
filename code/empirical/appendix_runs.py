"""Training runs for Appendix B.

Each run is one job, saved as output/runs/appendix_b/<job>.json, so that several workers can
share the list and an interrupted run can resume. Usage:

    python appendix_runs.py list            # print the jobs and whether they are done
    python appendix_runs.py work [threads]  # take unfinished jobs one at a time until none is left

Run several workers in parallel to use more cores. `appendix_tables.py` summarizes the results.
"""
import json
import os
import random
import sys
import time
import warnings

import numpy as np
import pandas as pd
import torch

warnings.filterwarnings("ignore")
from sdv.metadata import Metadata                                              # noqa: E402
from sdv.single_table import (GaussianCopulaSynthesizer, CTGANSynthesizer,     # noqa: E402
                              TVAESynthesizer)

import common as C                                                             # noqa: E402
import datasets as D                                                           # noqa: E402

SYNTH = {"CTGAN": CTGANSynthesizer, "TVAE": TVAESynthesizer,
         "Gaussian copula": GaussianCopulaSynthesizer}
SDV3 = ["CTGAN", "TVAE", "Gaussian copula"]
TEXTBOOK = list(C.TEXTBOOK)
N_SYN = C.N_SYN


def seed_all(s):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)


def sample(model, x, seed, n=N_SYN, **kw):
    """Trains `model` on x and returns n synthetic losses. SDV models reproduce
    sdv_models.sdv_sample."""
    if model in TEXTBOOK:
        return C.textbook_sample(model, x, seed, n=n, **kw)
    seed_all(seed)
    df = pd.DataFrame({"loss": x})
    md = Metadata.detect_from_dataframes({"losses": df})
    s = SYNTH[model](md, **kw)
    s.fit({"losses": df})
    seed_all(seed + 7)
    o = s.sample(n)
    o = o["losses"] if isinstance(o, dict) else o
    out = o["loss"].to_numpy(dtype=float)
    return out


# Job list
HYPER = [  # (label, model, keyword arguments)
    ("CTGAN, 100 epochs", "CTGAN", {"epochs": 100}),
    ("CTGAN, 1,000 epochs", "CTGAN", {"epochs": 1000}),
    ("CTGAN, 3,000 epochs", "CTGAN", {"epochs": 3000}),
    ("CTGAN, batch size 100", "CTGAN", {"batch_size": 100}),
    ("CTGAN, layers of 64", "CTGAN", {"generator_dim": (64, 64), "discriminator_dim": (64, 64)}),
    ("CTGAN, layers of 512", "CTGAN",
     {"generator_dim": (512, 512), "discriminator_dim": (512, 512)}),
    ("TVAE, 100 epochs", "TVAE", {"epochs": 100}),
    ("TVAE, 1,000 epochs", "TVAE", {"epochs": 1000}),
    ("TVAE, 3,000 epochs", "TVAE", {"epochs": 3000}),
    ("TVAE, layers of 256", "TVAE", {"compress_dims": (256, 256), "decompress_dims": (256, 256)}),
    ("Copula, normal marginal", "Gaussian copula", {"default_distribution": "norm"}),
    ("Copula, truncated normal marginal", "Gaussian copula",
     {"default_distribution": "truncnorm"}),
    ("Copula, gamma marginal", "Gaussian copula", {"default_distribution": "gamma"}),
]


def jobs():
    J = []
    # One round of training: Danish data with 100 seeds (5 for our own models), other datasets with 5
    for ds, seeds in [("danish", range(1, 101)), ("norwegian", range(1, 6)), ("soa", range(1, 6)),
                      ("sp500", range(1, 6))]:
        for model in SDV3 + TEXTBOOK:
            for s in seeds:
                if model in TEXTBOOK and ds == "danish" and s > 5:
                    continue
                J.append(dict(kind="one", ds=ds, model=model, seed=s))
    # Other settings on the Danish data, 5 seeds each
    for label, model, kw in HYPER:
        for s in range(1, 6):
            J.append(dict(kind="hyper", ds="danish", model=model, seed=s, label=label, kw=kw))
    # Recursive training on the Danish data
    for model in SDV3:
        for s in range(51, 59):
            J.append(dict(kind="rec", ds="danish", model=model, seed=s, ratio=1.0, gens=10))
        for r in (0.5, 2.0):
            for s in range(61, 66):
                J.append(dict(kind="rec", ds="danish", model=model, seed=s, ratio=r, gens=6))
        for nsub in (500, 1000):
            for s in range(71, 76):
                J.append(dict(kind="rec", ds="danish", model=model, seed=s, ratio=1.0, gens=8,
                              nsub=nsub))
    # Recursive training on the other datasets
    for ds in ("norwegian", "soa", "sp500"):
        for model in SDV3:
            for s in range(81, 84):
                J.append(dict(kind="rec", ds=ds, model=model, seed=s, ratio=1.0, gens=6))
    # a fourth CTGAN run on the medical claims
    J.append(dict(kind="rec", ds="soa", model="CTGAN", seed=84, ratio=1.0, gens=6))
    for j in J:
        parts = [j["kind"], j["ds"], j.get("label", j["model"]), f"s{j['seed']}"]
        if j["kind"] == "rec":
            parts += [f"r{j['ratio']}", f"g{j['gens']}"] + ([f"n{j['nsub']}"] if "nsub" in j else [])
        j["id"] = "__".join(p.replace(" ", "_").replace(",", "") for p in parts)
    return J


def cost(j):
    """Rough relative cost, used to start long jobs first."""
    size = {"danish": 1, "norwegian": 4, "soa": 4.5, "sp500": 1.8}[j["ds"]]
    c = {"Gaussian copula": 0.1}.get(j["model"], 1.0)
    if j["kind"] == "rec":
        n = j.get("nsub", 2167) / 2167
        c *= j["gens"] * (1 + j["ratio"]) * n
    if j["kind"] == "hyper":
        c *= j["kw"].get("epochs", 300) / 300
    return c * size


# Running a job
def run(j):
    ds = D.Dataset(j["ds"])
    kw = dict(j.get("kw", {}))
    if j["kind"] in ("one", "hyper"):
        xs = sample(j["model"], ds.x, j["seed"], **kw)
        np.save(D.SAMPLES / f"{j['id']}.npy", xs.astype(np.float32))
        return {"stats": ds.tail_stats(xs)}
    x_real = ds.x
    if "nsub" in j:
        x_real = np.random.default_rng(j["seed"]).choice(ds.x, j["nsub"], replace=False)

    def fn(x, s):
        return sample(j["model"], x, s, **kw)
    return D.recursion(ds, fn, j["seed"], j["gens"], j["ratio"], x_real=x_real)


def work(threads):
    torch.set_num_threads(threads)
    for j in sorted(jobs(), key=cost, reverse=True):
        out = D.RAW / f"{j['id']}.json"
        lock = D.RAW / f"{j['id']}.lock"
        if out.exists():
            continue
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            continue
        os.close(fd)
        t0 = time.time()
        try:
            res = run(j)
            res.update(job=j, seconds=time.time() - t0)
            out.write_text(json.dumps(res))
            print(f"done {j['id']} in {time.time() - t0:.0f}s", flush=True)
        except Exception as e:                       # keep the worker going; report at the end
            print(f"FAILED {j['id']}: {e!r}", flush=True)
        finally:
            lock.unlink(missing_ok=True)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        J = jobs()
        done = sum((D.RAW / f"{j['id']}.json").exists() for j in J)
        print(f"{len(J)} jobs, {done} done, relative cost {sum(map(cost, J)):.0f}")
    elif cmd == "work":
        work(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
