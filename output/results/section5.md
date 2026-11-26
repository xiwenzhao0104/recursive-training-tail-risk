# Section 5

## Table 1
model | P(>x0) | h(1%) | h(0.5%) | h(0.2%) | implied gamma (1%) | largest loss
Real losses | 10.0 | 1.02 | 0.51 | 0.23 | -- | 263
CTGAN (SDV) | 10.1 | 0.56 | 0.08 | 0.01 | 1.25 | 86
TVAE (SDV) | 2.5 | 0.00 | 0.00 | 0.00 | -- | 17
Gaussian copula (SDV) | 16.7 | 0.08 | 0.01 | 0.00 | 2.12 | 55
GAN (textbook, log losses) | 9.9 | 1.10 | 0.69 | 0.30 | 0.96 | 1933
VAE (textbook, log losses) | 9.3 | 0.88 | 0.51 | 0.19 | 1.05 | 773
Gaussian mixture (textbook, log losses) | 9.7 | 1.15 | 0.61 | 0.16 | 0.94 | 361

## Figure 1(b)
CTGAN, m/n = 1: predicted 0.88, simulated 0.83
TVAE, m/n = 1: predicted 0.51, simulated 0.53
Gaussian copula, m/n = 1: predicted 0.53, simulated 0.52
GAN, m/n = 0.5: predicted 1.10, simulated 1.01
GAN, m/n = 1: predicted 1.69, simulated 1.19
GAN, m/n = 2: predicted 1.49, simulated 1.22
VAE, m/n = 0.5: predicted 0.96, simulated 0.86
VAE, m/n = 1: predicted 0.88, simulated 0.84
VAE, m/n = 2: predicted 0.83, simulated 0.72
Gaussian mixture, m/n = 0.5: predicted 1.10, simulated 0.97
Gaussian mixture, m/n = 1: predicted 1.14, simulated 1.09
Gaussian mixture, m/n = 2: predicted 1.47, simulated 1.26

## Textbook generative models and the tail of Danish fire losses
Real: n = 2167, x0 = 5.54, u(1.0%) = 26.04, u(0.5%) = 34.82, u(0.2%) = 57.02, Hill top 10% = 1.40, max = 263
Bootstrap 90% interval for the real Hill index: 1.26-1.56

## One round, log losses (median over 5 seeds)
model | P(>x0) | h(1%) | h(0.5%) | h(0.2%) | implied gamma (1%) | Hill top 10% | max
GAN | 0.099 | 0.0110 | 0.0069 | 0.0030 | 0.96 | 1.45 | 1933
VAE | 0.093 | 0.0088 | 0.0051 | 0.0019 | 1.05 | 1.51 | 773
Gaussian mixture | 0.097 | 0.0115 | 0.0061 | 0.0016 | 0.94 | 1.32 | 361

## GAN of other sizes, log losses (median over 3 seeds)
model | P(>x0) | h(1%) | h(0.5%) | h(0.2%) | implied gamma (1%) | Hill top 10% | max
GAN, width 32 | 0.089 | 0.0117 | 0.0074 | 0.0031 | 0.93 | 1.40 | 944
GAN, width 128 | 0.090 | 0.0105 | 0.0066 | 0.0029 | 0.98 | 1.42 | 1389

## Recursive training, log losses (m/n = 1: 8 generations, 3 seeds; m/n = 0.5 and 2: 6 generations, 2 seeds)
GAN, m/n = 1.0: one-round ratio 1.40, Proposition 1 fixed point 1.686%, simulated long run 1.192%
GAN, m/n = 0.5: one-round ratio 1.16, Proposition 1 fixed point 1.103%, simulated long run 1.005%
GAN, m/n = 2.0: one-round ratio 1.16, Proposition 1 fixed point 1.490%, simulated long run 1.218%
VAE, m/n = 1.0: one-round ratio 0.85, Proposition 1 fixed point 0.883%, simulated long run 0.838%
VAE, m/n = 0.5: one-round ratio 0.89, Proposition 1 fixed point 0.961%, simulated long run 0.862%
VAE, m/n = 2.0: one-round ratio 0.89, Proposition 1 fixed point 0.828%, simulated long run 0.723%
Gaussian mixture, m/n = 1.0: one-round ratio 1.11, Proposition 1 fixed point 1.138%, simulated long run 1.090%
Gaussian mixture, m/n = 0.5: one-round ratio 1.15, Proposition 1 fixed point 1.100%, simulated long run 0.974%
Gaussian mixture, m/n = 2.0: one-round ratio 1.15, Proposition 1 fixed point 1.466%, simulated long run 1.256%

## SDV synthesizers: one round of training (median over 5 seeds)
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

## SDV synthesizers: other settings (median over 3 seeds)
model | P(>x0) | h(1%) | h(0.5%) | h(0.2%) | implied gamma (1%) | Hill top 10% | max
CTGAN, 1,000 epochs | 0.091 | 0.0086 | 0.0042 | 0.0005 | 1.06 | 1.43 | 84
TVAE, 1,000 epochs | 0.075 | 0.0058 | 0.0003 | 0.0000 | 1.24 | 1.62 | 82
copula, kernel marginal | 0.133 | 0.0092 | 0.0046 | 0.0022 | 1.03 | 1.60 | 263

## CTGAN recursion with 1,000 epochs (m/n = 1, 6 generations, 4 seeds)
   seed 41: estimate 0.0102 0.0072 0.0092 0.0095 0.0102 0.0078 0.0067 | h 0.0052 0.0094 0.0096 0.0086 0.0056 0.0056 0.0009
   seed 42: estimate 0.0102 0.0074 0.0085 0.0095 0.0083 0.0088 0.0099 | h 0.0079 0.0050 0.0064 0.0075 0.0057 0.0096 0.0112
   seed 43: estimate 0.0102 0.0097 0.0090 0.0122 0.0113 0.0132 0.0106 | h 0.0115 0.0061 0.0113 0.0110 0.0159 0.0098 0.0078
   seed 44: estimate 0.0102 0.0115 0.0097 0.0115 0.0081 0.0097 0.0095 | h 0.0109 0.0086 0.0136 0.0061 0.0094 0.0051 0.0057
CTGAN, 1,000 epochs: one-round ratio 0.87, Proposition 1 fixed point 0.900%, simulated long run 0.950%
