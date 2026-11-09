# Textbook generative models and the tail of Danish fire losses
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

Total time 548s
