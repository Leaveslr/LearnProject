# Factor Backtest Pitfalls

## Core Claim

A single-factor backtest is useful as a research signal, but it is not a strategy proof. The result becomes meaningful only after checking data leakage, universe construction, turnover, costs, and robustness across market regimes.

## Mental Model

Treat a backtest like a lab experiment:

- The factor is the hypothesis.
- The universe is the sample.
- Costs and execution are the friction.
- Out-of-sample performance is the replication test.

## Checklist

- Avoid future information in feature construction.
- Rebuild the historical universe as it existed at the time.
- Measure turnover and transaction costs before celebrating returns.
- Compare across bull, bear, and sideways regimes.
- Keep a holdout period that is not touched during factor tuning.

## Content Angle

"Why your factor backtest looks profitable but cannot make money" works well as a beginner-friendly post or short video because the pain point is concrete and the lesson is reusable.
