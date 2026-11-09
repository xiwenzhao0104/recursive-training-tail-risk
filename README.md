# Replication package for "Recursive Training on Synthetic Data and Tail-Risk Pricing"

Xiwen Zhao

This package reproduces all figures, tables, and numerical results in the paper. The code is
written in Python 3.11, and `requirements.txt` lists the versions of the packages that were used
to produce the results. R and curl are also needed to obtain the data. After installing the
packages with `pip install -r requirements.txt`, the whole package can be run with
`bash run_all.sh`. The full run takes about two hours on a laptop, almost all of which is spent
training the synthetic-data tools in `sdv_models.py`. Figures are saved in `output/figures` and
numerical results in `output/results`.

## Data

The paper uses the Danish fire insurance database, which contains the 2,167 losses above
DKK 1 million recorded between 1980 and 1990. The data are distributed with the R package evir
(version 1.7-4) under the GPL-2 licence, so they are not included here. The script
`data/get_danish_data.sh` downloads evir from CRAN and saves the losses in `data/danish.csv`, and
`run_all.sh` calls it automatically if this file is missing.

## Code

The model is in `code/model.py`. The script `code/theory_figures.py` produces Figures 2 to 5, and
`code/theory_results.py` produces Table 3 and the other numbers reported in Sections 3, 4, and 6
to 9 and in the Appendix. Both scripts run in under a minute and reproduce the numbers in the
paper exactly.

The empirical results in Section 5 come from the scripts in `code/empirical`. The file
`common.py` loads the data, sets the thresholds, and defines the GAN, VAE, and Gaussian mixture
that we train ourselves. `textbook_models.py` trains these three models, while `sdv_models.py`
trains CTGAN, TVAE, and the Gaussian copula from the SDV library. `evidence_figure.py` then uses
the results of both scripts to produce Figure 1 and Table 1, so it must be run after them.

All random seeds are fixed. The results of the neural networks may nevertheless differ slightly
on other hardware or with other versions of the libraries.
