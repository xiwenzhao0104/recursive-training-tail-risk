# Appendix B: empirical results

## Appendix B.8: one round of training, by dataset (medians over seeds)
Columns: share above 90th / 99th / 99.5th / 99.8th percentile (percent), implied gamma, s.d. across seeds of the share above the 99th percentile, share of seeds below the real frequency, Hill index (top 10%), largest loss relative to the largest real loss
### Danish fire (n = 2167; 22 real losses above the 99th percentile, 95% interval for their frequency 0.64-1.53%; Hill index 1.40)
CTGAN (100 seeds) | 9.2 | 0.57 | 0.12 | 0.02 | 1.25 | 0.50 | 73% | 1.56 | 0.32
TVAE (100 seeds) | 2.6 | 0.00 | 0.00 | 0.00 | -- | 0.00 | 100% | 3.44 | 0.06
Gaussian copula (100 seeds) | 16.7 | 0.08 | 0.01 | 0.00 | 2.12 | 0.00 | 100% | 2.76 | 0.21
GAN (5 seeds) | 9.9 | 1.10 | 0.69 | 0.30 | 0.96 | 0.10 | 20% | 1.45 | 7.34
VAE (5 seeds) | 9.3 | 0.88 | 0.51 | 0.19 | 1.05 | 0.05 | 100% | 1.51 | 2.93
Gaussian mixture (5 seeds) | 9.7 | 1.15 | 0.61 | 0.16 | 0.94 | 0.03 | 0% | 1.32 | 1.37

### Norwegian fire (n = 9181; 92 real losses above the 99th percentile, 95% interval for their frequency 0.81-1.23%; Hill index 1.32)
CTGAN (5 seeds) | 10.6 | 1.09 | 0.34 | 0.00 | 0.96 | 0.29 | 40% | 1.36 | 0.13
TVAE (5 seeds) | 10.5 | 0.34 | 0.06 | 0.00 | 1.46 | 0.12 | 100% | 1.78 | 0.15
Gaussian copula (5 seeds) | 14.6 | 0.03 | 0.00 | 0.00 | 2.60 | 0.00 | 100% | 2.60 | 0.08
GAN (5 seeds) | 10.0 | 0.98 | 0.47 | 0.16 | 1.01 | 0.44 | 60% | 1.35 | 2.64
VAE (5 seeds) | 9.3 | 0.79 | 0.36 | 0.10 | 1.10 | 0.05 | 100% | 1.41 | 1.48
Gaussian mixture (5 seeds) | 10.8 | 0.72 | 0.21 | 0.02 | 1.14 | 0.02 | 100% | 1.41 | 0.46

### SOA medical (n = 10000; 100 real losses above the 99th percentile, 95% interval for their frequency 0.81-1.21%; Hill index 2.02)
CTGAN (5 seeds) | 9.7 | 0.98 | 0.39 | 0.02 | 1.01 | 0.24 | 60% | 2.12 | 0.36
TVAE (5 seeds) | 9.7 | 0.56 | 0.29 | 0.06 | 1.25 | 0.24 | 100% | 2.23 | 0.40
Gaussian copula (5 seeds) | 12.3 | 0.15 | 0.01 | 0.00 | 1.83 | 0.00 | 100% | 3.20 | 0.33
GAN (5 seeds) | 9.7 | 1.12 | 0.53 | 0.20 | 0.95 | 0.37 | 40% | 1.92 | 2.02
VAE (5 seeds) | 9.1 | 0.85 | 0.36 | 0.11 | 1.07 | 0.04 | 100% | 2.05 | 1.68
Gaussian mixture (5 seeds) | 11.3 | 0.63 | 0.15 | 0.02 | 1.20 | 0.01 | 100% | 2.34 | 0.69

### S&P 500 daily losses (n = 3975; 40 real losses above the 99th percentile, 95% interval for their frequency 0.72-1.37%; Hill index 3.13)
CTGAN (5 seeds) | 11.6 | 0.89 | 0.43 | 0.00 | 1.05 | 0.44 | 60% | 3.06 | 0.20
TVAE (5 seeds) | 7.8 | 0.46 | 0.21 | 0.00 | 1.34 | 0.08 | 100% | 3.43 | 0.19
Gaussian copula (5 seeds) | 10.9 | 1.06 | 0.51 | 0.06 | 0.97 | 0.00 | 0% | 3.23 | 0.36
GAN (5 seeds) | 11.0 | 1.03 | 0.55 | 0.10 | 0.99 | 0.64 | 40% | 3.30 | 0.52
VAE (5 seeds) | 10.3 | 1.45 | 0.90 | 0.27 | 0.84 | 0.04 | 0% | 2.76 | 1.15
Gaussian mixture (5 seeds) | 9.8 | 1.03 | 0.62 | 0.21 | 0.99 | 0.01 | 0% | 3.08 | 2.27

## Table B8: variation across training runs, Danish data, 100 seeds
model | mean share above 99th pct (%) | s.d. | 95% interval for the mean | min-max | implied gamma: median, interquartile range
CTGAN | 0.77 | 0.50 | 0.67-0.87 | 0.12-2.54 | 1.25, 0.99-1.41
TVAE | 0.00 | 0.00 | 0.00-0.00 | 0.00-0.04 | --, -----
Gaussian copula | 0.08 | 0.00 | 0.08-0.08 | 0.08-0.08 | 2.12, 2.12-2.12

## Table B9: other settings, Danish data (medians over 5 seeds)
setting | 90th | 99th | 99.5th | 99.8th (percent) | implied gamma | Hill top 10% | max loss
CTGAN, 100 epochs (5) | 7.1 | 0.09 | 0.03 | 0.01 | 2.03 | 3.02 | 89
CTGAN, 1,000 epochs (5) | 9.1 | 0.86 | 0.42 | 0.06 | 1.06 | 1.43 | 84
CTGAN, 3,000 epochs (5) | 8.8 | 0.86 | 0.33 | 0.04 | 1.06 | 1.41 | 80
CTGAN, batch size 100 (5) | 7.2 | 0.72 | 0.39 | 0.04 | 1.14 | 1.52 | 81
CTGAN, layers of 64 (5) | 14.4 | 0.32 | 0.12 | 0.03 | 1.49 | 1.98 | 95
CTGAN, layers of 512 (5) | 10.0 | 0.88 | 0.47 | 0.10 | 1.05 | 1.59 | 83
TVAE, 100 epochs (5) | 0.6 | 0.00 | 0.00 | 0.00 | -- | 4.94 | 8
TVAE, 1,000 epochs (5) | 7.5 | 0.58 | 0.03 | 0.00 | 1.24 | 1.62 | 85
TVAE, 3,000 epochs (5) | 9.5 | 0.57 | 0.10 | 0.07 | 1.24 | 1.54 | 93
TVAE, layers of 256 (5) | 2.9 | 0.00 | 0.00 | 0.00 | -- | 3.54 | 26
Copula, normal marginal (5) | 40.1 | 0.37 | 0.01 | 0.00 | 1.43 | 4.33 | 45
Copula, truncated normal marginal (5) | 60.7 | 0.45 | 0.01 | 0.00 | 1.35 | 5.02 | 45
Copula, gamma marginal (5) | 0.0 | 0.00 | 0.00 | 0.00 | -- | 6.72 | 14

## Appendix B.10: implied gamma under other reference and tail levels, and Hill-based gamma (Danish)
Real Hill index by share of the sample used: 2.5%: 1.85, 5%: 1.60, 10%: 1.40, 15%: 1.44, 20%: 1.43
   90% bootstrap intervals: 2.5%: 1.48-2.43, 5%: 1.33-1.84, 10%: 1.26-1.56, 15%: 1.32-1.58, 20%: 1.34-1.57
model | gamma from frequencies, reference level / tail level: 90th/99th (baseline), 95th/99th, 80th/99th, 90th/99.5th | gamma as ratio of Hill indices (top 5%, 10%, 20%) | 90% bootstrap interval of the baseline gamma (thresholds resampled)
CTGAN | 1.25, 1.35, 1.19, 1.47 | 1.09, 1.12, 1.15 | 0.98-1.46
TVAE | --, --, --, -- | 2.36, 2.46, 1.67 | 0/300 finite
Gaussian copula | 2.12, 2.60, 1.86, 2.39 | 2.13, 1.97, 1.47 | 1.60-2.44

## Table B10: recursive training, predicted and simulated long-run estimates
dataset | model | m/n | real draws | seeds | generations | real frequency (%) | one-round ratio | predicted (%) | simulated, mean of last 3 generations (%) | s.e. across seeds | simulated / predicted
Danish fire | CTGAN | 0.5 | 2167 | 5 | 6 | 1.02 | 1.04 | 1.03 | 0.99 | 0.08 | 0.96
Danish fire | CTGAN | 1 | 2167 | 8 | 10 | 1.02 | 1.06 | 1.08 | 0.89 | 0.08 | 0.83
Danish fire | CTGAN | 1 | 500 | 5 | 8 | 1.00 | 0.58 | 0.70 | 0.93 | 0.44 | 1.33
Danish fire | CTGAN | 1 | 1000 | 5 | 8 | 0.94 | 1.01 | 0.95 | 0.76 | 0.13 | 0.80
Danish fire | CTGAN | 2 | 2167 | 5 | 6 | 1.02 | 1.04 | 1.10 | 0.99 | 0.15 | 0.90
Danish fire | TVAE | 0.5 | 2167 | 5 | 6 | 1.02 | 0.00 | 0.68 | 0.71 | 0.02 | 1.05
Danish fire | TVAE | 1 | 2167 | 8 | 10 | 1.02 | 0.00 | 0.51 | 0.59 | 0.03 | 1.15
Danish fire | TVAE | 1 | 500 | 5 | 8 | 1.00 | 0.00 | 0.50 | 0.50 | 0.08 | 1.00
Danish fire | TVAE | 1 | 1000 | 5 | 8 | 0.94 | 0.00 | 0.47 | 0.47 | 0.04 | 1.00
Danish fire | TVAE | 2 | 2167 | 5 | 6 | 1.02 | 0.00 | 0.34 | 0.37 | 0.03 | 1.10
Danish fire | Gaussian copula | 0.5 | 2167 | 5 | 6 | 1.02 | 0.07 | 0.69 | 0.68 | 0.00 | 0.98
Danish fire | Gaussian copula | 1 | 2167 | 8 | 10 | 1.02 | 0.07 | 0.53 | 0.62 | 0.06 | 1.17
Danish fire | Gaussian copula | 1 | 500 | 5 | 8 | 1.00 | 0.10 | 0.53 | 0.53 | 0.09 | 1.01
Danish fire | Gaussian copula | 1 | 1000 | 5 | 8 | 0.94 | 0.20 | 0.52 | 0.52 | 0.06 | 0.99
Danish fire | Gaussian copula | 2 | 2167 | 5 | 6 | 1.02 | 0.07 | 0.36 | 0.37 | 0.01 | 1.04
Norwegian fire | CTGAN | 1 | 9181 | 3 | 6 | 1.00 | 1.01 | 1.01 | 1.07 | 0.07 | 1.05
Norwegian fire | TVAE | 1 | 9181 | 3 | 6 | 1.00 | 0.38 | 0.62 | 0.60 | 0.02 | 0.98
Norwegian fire | Gaussian copula | 1 | 9181 | 3 | 6 | 1.00 | 0.02 | 0.51 | 0.51 | 0.00 | 1.01
SOA medical | CTGAN | 1 | 10000 | 4 | 6 | 1.00 | 1.12 | 1.13 | 1.09 | 0.03 | 0.96
SOA medical | TVAE | 1 | 10000 | 3 | 6 | 1.00 | 0.76 | 0.81 | 0.98 | 0.05 | 1.22
SOA medical | Gaussian copula | 1 | 10000 | 3 | 6 | 1.00 | 0.15 | 0.54 | 0.62 | 0.10 | 1.15
S&P 500 daily losses | CTGAN | 1 | 3975 | 3 | 6 | 1.01 | 0.81 | 0.85 | 0.94 | 0.05 | 1.11
S&P 500 daily losses | TVAE | 1 | 3975 | 3 | 6 | 1.01 | 0.36 | 0.62 | 0.83 | 0.07 | 1.34
S&P 500 daily losses | Gaussian copula | 1 | 3975 | 3 | 6 | 1.01 | 1.05 | 1.06 | 0.79 | 0.04 | 0.75
Across 24 cells, simulated/real on predicted/real: slope 0.77, intercept 0.17, correlation 0.88; mean absolute gap 8.2 percent of the real frequency; share of cells with simulated below real frequency 92%
Path by generation (mean across seeds, percent), m/n = 1, full Danish data, 10 generations:
   CTGAN: 1.02 1.02 0.85 0.85 0.78 0.83 0.89 0.99 0.95 0.80 0.91
   TVAE: 1.02 0.51 0.56 0.54 0.54 0.53 0.56 0.58 0.61 0.56 0.59
   Gaussian copula: 1.02 0.53 0.56 0.55 0.54 0.57 0.58 0.57 0.54 0.61 0.70

## Table B7, last two columns, and Appendix B.12: long-run bias implied by each dataset (p* = 1%, p0 = 10%, spread 2.7 x p)
dataset | model | implied gamma (median over seeds) | long-run estimate at m/n = 0.5, 1, 2 (%) | relative bias at m/n = 1 (%) | spread bias at m/n = 1 (bp, positive = understated) | rarest level: gamma implied at the 99.8th percentile and relative bias of a 0.2% probability at m/n = 1 (%)
Danish fire | CTGAN | 1.25 | 0.81, 0.67, 0.49 | 33 | 88 | 1.63, 49
Danish fire | TVAE | -- | 0.67, 0.50, 0.33 | 50 | 135 | --, 50
Danish fire | Gaussian copula | 2.12 | 0.68, 0.51, 0.34 | 49 | 133 | --, 50
Danish fire | GAN | 0.96 | 1.05, 1.11, 1.23 | -11 | -30 | 0.90, -68
Danish fire | VAE | 1.05 | 0.94, 0.89, 0.80 | 11 | 30 | 1.01, 5
Danish fire | Gaussian mixture | 0.94 | 1.08, 1.17, 1.36 | -17 | -45 | 1.05, 16
Norwegian fire | CTGAN | 0.96 | 1.05, 1.10, 1.20 | -10 | -26 | --, 50
Norwegian fire | TVAE | 1.46 | 0.74, 0.58, 0.39 | 42 | 114 | 2.02, 50
Norwegian fire | Gaussian copula | 2.60 | 0.67, 0.50, 0.33 | 50 | 134 | --, 50
Norwegian fire | GAN | 1.01 | 0.99, 0.98, 0.97 | 2 | 5 | 1.06, 17
Norwegian fire | VAE | 1.10 | 0.90, 0.82, 0.68 | 18 | 49 | 1.17, 34
Norwegian fire | Gaussian mixture | 1.14 | 0.87, 0.76, 0.60 | 24 | 64 | 1.53, 48
SOA medical | CTGAN | 1.01 | 0.99, 0.98, 0.96 | 2 | 5 | 1.66, 49
SOA medical | TVAE | 1.25 | 0.81, 0.67, 0.49 | 33 | 89 | 1.32, 43
SOA medical | Gaussian copula | 1.83 | 0.69, 0.52, 0.35 | 48 | 129 | 2.53, 50
SOA medical | GAN | 0.95 | 1.06, 1.13, 1.27 | -13 | -35 | 1.00, 2
SOA medical | VAE | 1.07 | 0.93, 0.86, 0.75 | 14 | 37 | 1.14, 31
SOA medical | Gaussian mixture | 1.20 | 0.84, 0.71, 0.53 | 29 | 79 | 1.58, 48
S&P 500 daily losses | CTGAN | 1.05 | 0.95, 0.90, 0.81 | 10 | 28 | 2.18, 50
S&P 500 daily losses | TVAE | 1.34 | 0.78, 0.62, 0.43 | 38 | 102 | --, 50
S&P 500 daily losses | Gaussian copula | 0.97 | 1.03, 1.06, 1.13 | -6 | -17 | 1.33, 44
S&P 500 daily losses | GAN | 0.99 | 1.01, 1.03, 1.05 | -3 | -7 | 1.18, 35
S&P 500 daily losses | VAE | 0.84 | 1.25, 1.55, 2.23 | -55 | -147 | 0.92, -45
S&P 500 daily losses | Gaussian mixture | 0.99 | 1.01, 1.03, 1.06 | -3 | -8 | 0.99, -4


## Table B7: ratio of synthetic to real frequency by threshold, pooled over seeds
dataset | model | seeds | pooled h/p at 99th, 99.5th, 99.8th (90% interval over seeds, bootstrap) | share of seeds with h/p falling from 99th to 99.8th | max synthetic / max real (median) | Hill index synthetic / real (median, top 10%)
Danish fire | CTGAN | 100 | 0.75 (0.67-0.83) | 0.57 (0.47-0.69) | 0.25 (0.20-0.31) | 100% | 0.32 | 1.12
Danish fire | TVAE | 100 | 0.00 (0.00-0.00) | 0.00 (0.00-0.00) | 0.00 (0.00-0.00) | 5% | 0.06 | 2.46
Danish fire | Gaussian copula | 100 | 0.07 (0.07-0.07) | 0.02 (0.02-0.02) | 0.00 (0.00-0.00) | 100% | 0.21 | 1.97
Danish fire | GAN | 5 | 1.08 (1.01-1.13) | 1.36 (1.27-1.44) | 1.28 (1.16-1.39) | 0% | 7.34 | 1.04
Danish fire | VAE | 5 | 0.87 (0.83-0.90) | 1.02 (0.97-1.06) | 0.83 (0.78-0.87) | 100% | 2.93 | 1.08
Danish fire | Gaussian mixture | 5 | 1.14 (1.12-1.16) | 1.19 (1.17-1.21) | 0.71 (0.69-0.73) | 100% | 1.37 | 0.95
Norwegian fire | CTGAN | 5 | 1.01 (0.82-1.18) | 0.65 (0.49-0.81) | 0.00 (0.00-0.00) | 100% | 0.13 | 1.03
Norwegian fire | TVAE | 5 | 0.33 (0.25-0.41) | 0.14 (0.09-0.19) | 0.02 (0.01-0.02) | 100% | 0.15 | 1.35
Norwegian fire | Gaussian copula | 5 | 0.02 (0.02-0.02) | 0.00 (0.00-0.00) | 0.00 (0.00-0.00) | 100% | 0.08 | 1.98
Norwegian fire | GAN | 5 | 1.05 (0.79-1.36) | 1.06 (0.72-1.46) | 0.91 (0.54-1.40) | 80% | 2.64 | 1.03
Norwegian fire | VAE | 5 | 0.80 (0.76-0.83) | 0.72 (0.69-0.75) | 0.49 (0.47-0.52) | 100% | 1.48 | 1.07
Norwegian fire | Gaussian mixture | 5 | 0.72 (0.70-0.73) | 0.41 (0.40-0.42) | 0.12 (0.12-0.13) | 100% | 0.46 | 1.07
SOA medical | CTGAN | 5 | 0.94 (0.78-1.09) | 0.78 (0.64-0.93) | 0.09 (0.06-0.13) | 100% | 0.36 | 1.05
SOA medical | TVAE | 5 | 0.60 (0.44-0.77) | 0.57 (0.39-0.75) | 0.27 (0.20-0.34) | 80% | 0.40 | 1.10
SOA medical | Gaussian copula | 5 | 0.15 (0.15-0.15) | 0.02 (0.02-0.02) | 0.00 (0.00-0.00) | 100% | 0.33 | 1.58
SOA medical | GAN | 5 | 1.10 (0.86-1.35) | 0.99 (0.71-1.27) | 0.88 (0.58-1.18) | 100% | 2.02 | 0.95
SOA medical | VAE | 5 | 0.85 (0.82-0.88) | 0.72 (0.69-0.75) | 0.57 (0.54-0.61) | 100% | 1.68 | 1.01
SOA medical | Gaussian mixture | 5 | 0.63 (0.62-0.63) | 0.30 (0.30-0.31) | 0.10 (0.10-0.11) | 100% | 0.69 | 1.16
S&P 500 daily losses | CTGAN | 5 | 0.98 (0.72-1.28) | 0.96 (0.66-1.30) | 0.02 (0.01-0.04) | 100% | 0.20 | 0.98
S&P 500 daily losses | TVAE | 5 | 0.44 (0.39-0.50) | 0.40 (0.34-0.46) | 0.00 (0.00-0.00) | 100% | 0.19 | 1.10
S&P 500 daily losses | Gaussian copula | 5 | 1.05 (1.05-1.05) | 1.00 (1.00-1.00) | 0.27 (0.27-0.27) | 100% | 0.36 | 1.03
S&P 500 daily losses | GAN | 5 | 1.17 (0.73-1.60) | 1.34 (0.79-1.93) | 0.79 (0.34-1.25) | 100% | 0.52 | 1.06
S&P 500 daily losses | VAE | 5 | 1.45 (1.42-1.48) | 1.80 (1.77-1.83) | 1.36 (1.31-1.40) | 100% | 1.15 | 0.88
S&P 500 daily losses | Gaussian mixture | 5 | 1.02 (1.02-1.03) | 1.23 (1.22-1.24) | 1.03 (1.00-1.06) | 40% | 2.27 | 0.99
Share of all runs in which h/p is lower at the 99.8th than at the 99th percentile: CTGAN 100% (115), TVAE 17% (115), Gaussian copula 100% (115), GAN 70% (20), VAE 100% (20), Gaussian mixture 85% (20)
