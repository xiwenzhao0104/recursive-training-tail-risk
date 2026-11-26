# Appendix B: theoretical robustness

## B.1 Alternative heavy-tailed distributions
GPD fitted to Danish losses above the 90th percentile: shape 0.58 (tail index 1.71), scale 4.51
Baseline one-round sampling rate at 1%: 0.794%
family | c | h(1%) | estimate at m/n = 0.5, 1, 2 | relative bias at m/n=1 for p* = 0.5%, 1%, 2% | max number of fixed points
Pareto (baseline) | c = 1.1 (1.100) | 0.794 | 0.90, 0.82, 0.68 | 21.7, 18.1, 13.9 | 1
Pareto (baseline) | matched (1.100) | 0.794 | 0.90, 0.82, 0.68 | 21.7, 18.1, 13.9 | 1
Lognormal | c = 1.1 (1.100) | 0.753 | 0.89, 0.79, 0.63 | 25.7, 21.4, 16.1 | 1
Lognormal | matched (1.082) | 0.794 | 0.90, 0.82, 0.68 | 22.4, 18.3, 13.5 | 1
Weibull | c = 1.1 (1.100) | 0.719 | 0.87, 0.76, 0.59 | 29.1, 24.0, 17.8 | 1
Weibull | matched (1.070) | 0.794 | 0.90, 0.82, 0.67 | 23.0, 18.4, 13.2 | 1
Generalized Pareto | c = 1.1 (1.100) | 0.906 | 0.95, 0.91, 0.84 | 12.6, 8.7, 4.9 | n.c.
Generalized Pareto | matched (1.247) | 0.794 | 0.91, 0.83, 0.71 | 23.6, 17.1, 10.0 | n.c.

## B.2 Uniqueness and stability
Lemma 1, gamma 1.01-3, p* 0.01%-9.9% (including above p-hat = 3.86%), m/n 0.1-200: largest number of fixed points 1
h is increasing and convex for the Pareto, lognormal and Weibull forms (checked numerically)

S-shaped h: Lemma 1 times a logistic cut-off at p_f with width s (no tail events once the estimate is well below p_f)
p_f = 0.6%, m/n = 0.5: 0.90% (stable) | collapsed level p*/(1+m/n) = 0.67%
p_f = 0.6%, m/n = 1.0: 0.50% (stable); 0.59% (unstable); 0.82% (stable) | collapsed level p*/(1+m/n) = 0.50%
p_f = 0.6%, m/n = 2.0: 0.33% (stable) | collapsed level p*/(1+m/n) = 0.33%
p_f = 0.7%, m/n = 0.5: 0.90% (stable) | collapsed level p*/(1+m/n) = 0.67%
p_f = 0.7%, m/n = 1.0: 0.50% (stable); 0.73% (unstable); 0.82% (stable) | collapsed level p*/(1+m/n) = 0.50%
p_f = 0.7%, m/n = 2.0: 0.33% (stable) | collapsed level p*/(1+m/n) = 0.33%

## B.3 Sensitivity to gamma and to the form of the tail-index gap
gamma | relative bias at m/n = 0.5, 1, 2 (exact) | first-order approximation
1.02 | 2.2, 4.4, 8.5 | 2.3, 4.4, 8.4
1.05 | 5.3, 10.2, 19.1 | 5.4, 10.3, 18.7
1.10 | 9.7, 18.1, 32.0 | 10.3, 18.7, 31.5
1.15 | 13.3, 24.3, 40.9 | 14.7, 25.7, 40.9
1.20 | 16.4, 29.1, 47.1 | 18.7, 31.5, 47.9
1.25 | 18.9, 32.9, 51.5 | 22.3, 36.5, 53.5
1.50 | 26.7, 43.2, 61.7 | 36.5, 53.5, 69.7
Additive gap: model tail index = learned index + kappa, kappa = 0.14 (same h(1%) as gamma = 1.1 when the learned index is 1.4)
   p* = 0.5%: one-round ratio 0.741; relative bias at m/n = 0.5, 1, 2: 11.5, 20.6, 34.1 | multiplicative: 11.8, 21.7, 36.9
   p* = 1.0%: one-round ratio 0.794; relative bias at m/n = 0.5, 1, 2: 9.3, 17.1, 29.1 | multiplicative: 9.7, 18.1, 32.0
   p* = 2.0%: one-round ratio 0.851; relative bias at m/n = 0.5, 1, 2: 6.9, 12.9, 22.9 | multiplicative: 7.2, 13.9, 25.8

## B.4 Weights on synthetic draws
weight | estimate at m/n = 0.5, 1, 2 | Section 4 calibration: data-rich, data-poor, cutoff (bp), states | spread 40 years after a 20-year calm (bp)
1.00 | 0.90, 0.82, 0.68 | 221, 66, 162, both | 66
0.75 | 0.93, 0.86, 0.74 | 232, 84, 110, both | 232
0.50 | 0.95, 0.90, 0.82 | 244, 115, 66, data-rich only | 244
0.25 | 0.97, 0.95, 0.90 | 257, 168, 32, data-rich only | 257
0.00 | 1.00, 1.00, 1.00 | 270, 270, 7, data-rich only | 270

## B.5 Dependence over time and changing exposure (m/n = 1, n = 2,000 on average)
case | mean real frequency in window | mean estimate | estimate / real frequency | deterministic fixed point / p* | s.d. of estimate
Independent draws (baseline) | 0.997 | 0.818 | 0.821 | 0.819 | 0.213
Log probability AR(1), persistence 0.5, s.d. 0.5 | 1.000 | 0.822 | 0.822 | 0.819 | 0.273
Log probability AR(1), persistence 0.9, s.d. 0.5 | 1.004 | 0.829 | 0.826 | 0.819 | 0.407
Two regimes, 0.5% and 1.5%, switching with prob. 0.1 a year | 1.003 | 0.827 | 0.824 | 0.819 | 0.337
Exposure growing 3% a year | 1.001 | 0.826 | 0.825 | 0.819 | 0.361
Clustering within years, intra-class correlation 0.05 | 1.001 | 0.829 | 0.828 | 0.819 | 0.478
Clustering within years, intra-class correlation 0.10 | 0.999 | 0.835 | 0.836 | 0.819 | 0.652

## B.6 Continuous choice of the length of history
The firm chooses T in [T_L, T_H] each year to minimize L p/(qT+m) + c(T).
linear cost:
   cost x 0.6: 221 bp (stable, T = 20.0 yrs)
   cost x 1.0: 66 bp (stable, T = 2.0 yrs); 67 bp (unstable, T = 2.0 yrs); 221 bp (stable, T = 20.0 yrs)
   cost x 1.5: 66 bp (stable, T = 2.0 yrs); 125 bp (unstable, T = 4.6 yrs); 180 bp (stable, T = 9.4 yrs)
   cost x 2.0: 66 bp (stable, T = 2.0 yrs)
   cost x 3.0: 66 bp (stable, T = 2.0 yrs)
   two stable states for cost multiples 0.99-1.57
   20-year calm (cost x 1): history falls to 2.0 years; spread 40 years after the calm 66 bp (history 2.0 years)

## B.7 Other objectives
Loss L|e|^1: perceived value of the history is proportional to p^0.5, so the cutoff rule holds
Loss L|e|^2: perceived value of the history is proportional to p^1, so the cutoff rule holds
Loss L|e|^4: perceived value of the history is proportional to p^2, so the cutoff rule holds
Naive firm cutoff 162 bp; firm that knows gamma: cutoff 7 bp (data-poor estimate 66 bp, data-rich 221 bp)
Two states exist for F/L between 4.99e-07 and 1.67e-06, a factor of 3.4; baseline F/L 1.23e-06

## B.8 Pricing functions (p* = 1%, m/n = 1)
pricing | true spread (bp) | long-run spread (bp) | bias (bp) | bias (% of true spread) | bias for p* = 0.5% and 2% (%)
Constant multiple 2.7 (baseline) | 270 | 221 | 49 | 18.1 | 21.7, 13.9
Multiple 2.0 (soft market) | 200 | 164 | 36 | 18.1 | 21.7, 13.9
Multiple 4.0 (hard market) | 400 | 327 | 73 | 18.1 | 21.7, 13.9
Lane (2000) | 669 | 597 | 72 | 10.7 | 12.5, 8.5
2.7 x p plus 100 bp for liquidity and maturity | 370 | 321 | 49 | 13.2 | 12.5, 11.7
Wang transform, lambda = 0.40 | 270 | 227 | 43 | 15.9 | 19.3, 12.0
Expected loss plus 0.171 s.d. | 270 | 236 | 34 | 12.7 | 14.4, 10.2
Three-year bond, 2.7 x annualized probability | 267 | 219 | 48 | 18.0 | 21.6, 13.6

## B.9 Minimum share of real data for a tolerated relative bias
The rule uses only the model's own estimate p and gamma, p0: m/n <= delta / ((1 - delta)(1 - theta(p)))
gamma | estimate | max m/n (min real share) for tolerated bias 5% | 10% | 20%
1.05 | 0.5% | 0.38 (73%) | 0.80 (56%) | 1.80 (36%)
1.05 | 1.0% | 0.48 (67%) | 1.02 (49%) | 2.30 (30%)
1.05 | 2.0% | 0.68 (59%) | 1.44 (41%) | 3.23 (24%)
1.10 | 0.5% | 0.20 (83%) | 0.43 (70%) | 0.97 (51%)
1.10 | 1.0% | 0.26 (80%) | 0.54 (65%) | 1.22 (45%)
1.10 | 2.0% | 0.35 (74%) | 0.75 (57%) | 1.68 (37%)
1.25 | 0.5% | 0.10 (91%) | 0.21 (83%) | 0.47 (68%)
1.25 | 1.0% | 0.12 (89%) | 0.25 (80%) | 0.57 (64%)
1.25 | 2.0% | 0.16 (86%) | 0.34 (75%) | 0.75 (57%)

## B.10 Policies under different market conditions (Section 4 calibration)
policy | gamma = 1.1: steady state, after a 20-year calm | gamma = 1.25: steady state, after a 20-year calm (long-run spread in bp; true spread 270)
No policy | 221, 66 | 181, 35
Minimum real share (20-year history) | 221, 221 | 181, 181
Tail validation (gamma = 1.02) | 258, 258 | 258, 258
Synthetic draws weighted 0.5 | 244, 244 | 219, 219
Subsidy (m from 2,000 to 3,000) | 45, 45 | 24, 24
Recent-data rule (last 5 years) | 132, 132 | 81, 81
Stochastic version, 1,000 observations a year: share of markets data-poor 40 years after a 20-year calm
   No policy: 1.00
   Minimum real share (20-year history): no maintenance choice
   Tail validation (gamma = 1.02): 0.01
   Synthetic draws weighted 0.5: 0.00
   Subsidy (m from 2,000 to 3,000): 1.00
   Recent-data rule (last 5 years): no maintenance choice
