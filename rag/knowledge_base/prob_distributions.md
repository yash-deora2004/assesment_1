# Probability — Distributions

## Binomial Distribution

A random variable X follows Binomial(n, p) if:
- n independent trials
- Each trial has two outcomes: success (probability p) or failure (probability q = 1−p)

**P(X = k) = C(n, k) · p^k · q^(n−k)**

- Mean: E(X) = np
- Variance: Var(X) = npq
- Standard deviation: σ = √(npq)

### Properties
- Most probable value (mode): floor((n+1)p) or floor((n+1)p) − 1
- For n large, p small, np moderate → approximate with Poisson

## Poisson Distribution

X ~ Poisson(λ) for rare events with average rate λ:

**P(X = k) = e^(−λ) · λ^k / k!**

- Mean: E(X) = λ
- Variance: Var(X) = λ

## Bernoulli Distribution

Special case of Binomial with n = 1:
- P(X = 1) = p, P(X = 0) = 1 − p
- Mean = p, Variance = p(1−p)

## Geometric Distribution

X = number of trials until first success:
- P(X = k) = (1−p)^(k−1) · p
- Mean = 1/p
- Variance = (1−p)/p²

## Expected Value and Variance

- **E(aX + b) = a·E(X) + b**
- **Var(aX + b) = a²·Var(X)**
- For independent X, Y: **Var(X + Y) = Var(X) + Var(Y)**

## JEE Tips

- Binomial distribution is by far the most tested distribution in JEE.
- For "at least k successes", compute 1 − P(X < k).
- Mean of binomial = np; if asked "expected number of successes", this is the answer.
