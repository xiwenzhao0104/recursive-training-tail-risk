# SDV synthesizers: one round of training (median over 5 seeds)
## SDV defaults
model | P(>x0) | h(1%) | h(0.5%) | h(0.2%) | implied gamma (1%) | Hill top 10% | max
CTGAN | 0.101 | 0.0056 | 0.0008 | 0.0001 | 1.25 | 1.63 | 86
TVAE | 0.025 | 0.0000 | 0.0000 | 0.0000 | inf | 3.73 | 17
Gaussian copula | 0.167 | 0.0008 | 0.0001 | 0.0000 | 2.12 | 2.76 | 55
## no clipping to the observed range
model | P(>x0) | h(1%) | h(0.5%) | h(0.2%) | implied gamma (1%) | Hill top 10% | max
CTGAN | 0.101 | 0.0056 | 0.0008 | 0.0001 | 1.25 | 1.63 | 86
TVAE | 0.025 | 0.0000 | 0.0000 | 0.0000 | inf | 3.73 | 17
Gaussian copula | 0.167 | 0.0008 | 0.0001 | 0.0000 | 2.12 | 2.76 | 55
