# Algebra — Logarithms

## Definition

log_b(a) = c means b^c = a, where b > 0, b ≠ 1, a > 0.

## Fundamental Properties

1. **log_b(xy) = log_b(x) + log_b(y)**
2. **log_b(x/y) = log_b(x) − log_b(y)**
3. **log_b(x^n) = n · log_b(x)**
4. **log_b(1) = 0**
5. **log_b(b) = 1**

## Change of Base Formula

**log_b(a) = log_c(a) / log_c(b)** = ln(a) / ln(b)

Special case: **log_b(a) = 1 / log_a(b)**

## Natural and Common Logarithms

- **ln(x)** = log_e(x), where e ≈ 2.71828
- **log(x)** = log₁₀(x) (common logarithm)

## Logarithmic Equations

- To solve log_b(f(x)) = c: convert to f(x) = b^c, then check domain f(x) > 0.
- To solve log_b(f(x)) = log_b(g(x)): set f(x) = g(x), then verify f(x) > 0 and g(x) > 0.

## Logarithmic Inequalities

- If b > 1: log_b(x) > log_b(y) ⟺ x > y > 0
- If 0 < b < 1: log_b(x) > log_b(y) ⟺ 0 < x < y (inequality reverses)

## JEE Tips

- Always check the domain: argument > 0 and base > 0, base ≠ 1.
- log_b(a) · log_a(b) = 1 is frequently tested.
- The number of digits in N = floor(log₁₀(N)) + 1.
- Characteristic of log₁₀(N) gives the number of digits minus 1.
