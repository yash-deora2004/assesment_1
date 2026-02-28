# Calculus — Limits

## Definition

lim(x→a) f(x) = L means f(x) gets arbitrarily close to L as x approaches a.

## Standard Limits

1. **lim(x→0) sin(x)/x = 1**
2. **lim(x→0) (1 − cos(x))/x² = 1/2**
3. **lim(x→0) tan(x)/x = 1**
4. **lim(x→0) (eˣ − 1)/x = 1**
5. **lim(x→0) ln(1 + x)/x = 1**
6. **lim(x→0) (aˣ − 1)/x = ln(a)**
7. **lim(x→0) (1 + x)^(1/x) = e**
8. **lim(x→∞) (1 + 1/x)^x = e**
9. **lim(x→a) (xⁿ − aⁿ)/(x − a) = n·a^(n−1)**

## Techniques for Evaluating Limits

### Direct Substitution
Try substituting x = a first. If no indeterminate form, that's the answer.

### Factoring
Factor numerator and denominator to cancel common terms.

### Rationalization
For expressions with square roots: multiply by conjugate.

### L'Hôpital's Rule
If lim(x→a) f(x)/g(x) gives 0/0 or ∞/∞:
**lim(x→a) f(x)/g(x) = lim(x→a) f'(x)/g'(x)**

Can be applied repeatedly if the resulting limit is still indeterminate.

### Squeeze Theorem
If g(x) ≤ f(x) ≤ h(x) near a, and lim g(x) = lim h(x) = L, then lim f(x) = L.

## Indeterminate Forms

0/0, ∞/∞, 0·∞, ∞−∞, 0⁰, ∞⁰, 1^∞

### Handling 1^∞ Form
lim f(x)^g(x) where f→1, g→∞:
= e^(lim g(x)·(f(x)−1))

## JEE Tips

- Memorize all standard limits — they appear in almost every limits question.
- For 1^∞ form, use the exponential trick: e^(lim g(x)·(f(x)−1)).
- L'Hôpital is powerful but can be slow; try algebraic simplification first.
- Check left-hand and right-hand limits separately when asked if a limit exists.
