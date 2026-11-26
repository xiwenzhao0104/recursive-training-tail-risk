# Replication package for "Synthetic Data, Recursive Training, and the Pricing of Tail Risk"

Xiwen Zhao

This package reproduces every figure, table and number in the paper, including Appendix B.

## Requirements and running time

- Python 3.11.9 with the packages in `requirements.txt` (numpy 2.4.6, scipy 1.17.1,
  pandas 2.3.3, matplotlib 3.11.2, torch 2.15.0, sdv 2.1.0). Install them with
  `pip install -r requirements.txt`, preferably in a virtual environment.
- R 4.5.1 and curl, used only to download and extract the data.
- The results in the paper were produced on an Apple M2 computer with 24 GB of
  memory, running macOS 15.8. Neural networks were trained on the CPU with one thread per process.

Run everything with

    bash run_all.sh 4

where the argument is the number of parallel processes used for the training runs of
Appendix B. The theoretical results take a few minutes. The Section 5 scripts take around two
hours, and the 582 training runs of Appendix B take around 9 CPU hours, or around 2 hours with
4 processes. 

## Data

All data are public and are downloaded by the scripts in `data/`, which `run_all.sh` calls if
the files are missing. They are not redistributed here.

| File | Content | Source |
|---|---|---|
| `danish.csv` | 2,167 Danish fire insurance losses above DKK 1 million, 1980-1990 | R package evir 1.7-4 (`get_danish_data.sh`) |
| `norwegian_fire.csv` | 9,181 Norwegian fire insurance claims, 1972-1992 | R package ReIns 1.0.16 (`get_extra_data.sh`) |
| `soa_medical.csv` | 75,789 SOA group medical claims above USD 25,000, 1991; the code draws a random sample of 10,000 with seed 0 | R package ReIns 1.0.16 |
| `sp500_losses.csv` | Losses of the S&P 500 index on the 3,975 trading days between 1960 and 1993 with a negative return, in percent | R package evir 1.7-4 (`sp.raw`) |

## Where each result comes from

`output/results` contains one file for each part of the paper, and `output/figures` the figures.
Intermediate files (the results of each training run and the synthetic samples) are written to
`output/runs`, which is not distributed.

| Result in the paper | Script | Output |
|---|---|---|
| Figures 2-5 | `code/theory_figures.py` | `output/figures/` |
| Table 3 and numbers in Sections 3, 4 and 6-9 and Appendix A | `code/theory_results.py` | `theory.md` |
| Table 4, Tables B1-B6 and numbers in Appendix B.1-B.7 | `code/theory_appendix.py` | `appendix_b_theory.md` |
| Table 1, Figure 1 and the robustness checks of Section 5 | `code/empirical/textbook_models.py`, `sdv_models.py`, then `evidence_figure.py` | `section5.md`, `output/figures/fig_evidence.pdf` |
| Tables B7-B10 and numbers in Sections 5 and 6 and Appendix B.8-B.12 | `code/empirical/appendix_runs.py`, then `appendix_tables.py` | `appendix_b_evidence.md` |

## Code

`code/model.py` contains the model: the sampling function h of Lemma 1, the map of equation (3),
its fixed point, and the simulations with binomial draws used in Sections 4, 6 and 7.

`code/empirical/common.py` loads the Danish data, sets the thresholds and defines our own GAN,
VAE and Gaussian mixture. `code/empirical/datasets.py` does the same for all four datasets.
`sdv_models.py` and `appendix_runs.py` train the SDV tools (CTGAN, TVAE and the Gaussian
copula). `appendix_runs.py` defines each training run of Appendix B as a job with a fixed seed and
saves its result as a separate file, so that several processes can share the list and an
interrupted run can be resumed. `python appendix_runs.py list` shows how many jobs are done.

## Model settings and random seeds

The SDV tools use the defaults of SDV 2.1.0 unless stated otherwise: 300 epochs, a batch size of
500 and two layers of 256 units for CTGAN; 300 epochs and two layers of 128 units for TVAE; beta
marginals for the Gaussian copula. The alternative settings of Table B9 are listed in `HYPER` in
`appendix_runs.py`. Each model generates 400,000 synthetic losses. Our own GAN, VAE and Gaussian
mixture are defined in `common.py` (4,000 training steps, batch size 256, Adam).

All seeds are fixed in the code. Before each SDV model is trained, the Python, NumPy and PyTorch
generators are seeded with the run's seed s, and with s + 7 before it generates synthetic losses.
In recursive training, generation g of a run with seed s is trained with seed 100 s + g.

| Results | Seeds |
|---|---|
| Table 1 and Figure 1(a), one round | 1-5 |
| Table B8 and Table B7 (Danish), one round | 1-100 (1-5 as in Table 1) |
| Table B7 (other datasets) and Table B9 | 1-5 |
| Figure 1(b), SDV tools | 31, 32; our own models 11-13 (m/n = 1) and 21, 22 (m/n = 0.5, 2) |
| CTGAN with 1,000 epochs, recursion (Section 5) | 41-44 |
| Table B10: Danish, m/n = 1 | 51-58 |
| Table B10: Danish, m/n = 0.5 and 2 | 61-65 |
| Table B10: Danish subsamples of 500 and 1,000 losses | 71-75 (also the seed of the subsample) |
| Table B10: other datasets | 81-83 (CTGAN on the medical claims also 84) |
| Simulations in `theory_results.py` and `theory_appendix.py` | given in each call |

The results of the neural networks may differ slightly on other hardware or with other versions
of the libraries. Rerunning the package on the machine above reproduces the paper exactly.
