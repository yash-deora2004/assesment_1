# JEE-Specific Tips, Shortcuts, and Common Traps

## General Exam Strategy

1. **Time management**: ~3 minutes per question in JEE Main.
2. **Easy first**: solve confident questions first, mark uncertain ones for review.
3. **Negative marking**: in MCQ, avoid random guessing; in numerical type, always attempt.
4. **Elimination**: for MCQs, eliminate 2 options first, then decide.

## Quick Calculation Shortcuts

### Algebraic Shortcuts
- To check if x = a is a root of p(x): compute p(a) directly.
- For symmetric expressions: substitute a = b to simplify.
- Sum of coefficients of (1 + x)ⁿ = 2ⁿ (put x = 1).

### Calculus Shortcuts
- Derivative at a point: if f(x) = xⁿ, f'(a) = naⁿ⁻¹.
- For definite integrals with symmetry: use even/odd properties.
- lim(x→0) sin(x)/x ≈ 1 for small x estimation.

### Probability Shortcuts
- Complement is often faster: P(at least 1) = 1 − P(0).
- For identical outcomes: use stars and bars.
- Binomial: expected value = np, variance = npq.

## Common JEE Traps

### Trap 1: Forgetting ±
- √(x²) = |x| not x
- Quadratic formula has ±
- sin⁻¹ and cos⁻¹ have restricted ranges

### Trap 2: Domain Errors
- log₂(x−1) requires x > 1
- Dividing by (x−a) loses the solution x = a
- tan(x) is undefined at odd multiples of π/2

### Trap 3: False Patterns
- (a + b)² ≠ a² + b²
- det(A + B) ≠ det(A) + det(B)
- f(a+b) ≠ f(a) + f(b) unless f is linear

### Trap 4: Incomplete Solutions
- Forgetting to check for extraneous roots after squaring
- Not considering all cases in absolute value equations
- Missing solutions in trigonometric equations (general solution)

## Topic-Wise Key Formulas (Quick Reference)

### Algebra
- Quadratic: x = (−b ± √(b²−4ac)) / 2a
- AM ≥ GM ≥ HM
- Sum of GP: a(rⁿ−1)/(r−1)

### Calculus
- Chain rule: d/dx[f(g(x))] = f'(g(x))·g'(x)
- By parts: ∫u dv = uv − ∫v du
- L'Hôpital: lim f/g = lim f'/g' (for 0/0 or ∞/∞)

### Probability
- Bayes: P(A|B) = P(B|A)·P(A) / P(B)
- Binomial: P(X=k) = C(n,k)·p^k·q^(n−k)
- nCr = n!/r!(n−r)!

### Linear Algebra
- det(AB) = det(A)·det(B)
- Cramer: xᵢ = det(Aᵢ)/det(A)
- A⁻¹ = adj(A)/det(A)

## Answer Verification Checklist

- [ ] Did I check the domain/range?
- [ ] Did I consider all cases?
- [ ] Did I substitute back to verify?
- [ ] Does the answer have the right sign?
- [ ] Does the answer make intuitive sense?
- [ ] Did I simplify completely?
