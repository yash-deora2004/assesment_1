# Calculus — Basic Integration

## Definition

∫f(x)dx = F(x) + C, where F'(x) = f(x)

## Basic Integration Formulas

| Function | Integral |
|---|---|
| xⁿ (n ≠ −1) | x^(n+1)/(n+1) + C |
| 1/x | ln\|x\| + C |
| eˣ | eˣ + C |
| aˣ | aˣ/ln(a) + C |
| sin(x) | −cos(x) + C |
| cos(x) | sin(x) + C |
| sec²(x) | tan(x) + C |
| csc²(x) | −cot(x) + C |
| sec(x)tan(x) | sec(x) + C |
| csc(x)cot(x) | −csc(x) + C |
| 1/√(1−x²) | sin⁻¹(x) + C |
| 1/(1+x²) | tan⁻¹(x) + C |

## Integration Techniques

### Substitution (u-substitution)
∫f(g(x))·g'(x)dx = ∫f(u)du where u = g(x)

### Integration by Parts
∫u·dv = uv − ∫v·du

**LIATE rule** for choosing u: Logarithmic, Inverse trig, Algebraic, Trigonometric, Exponential

### Partial Fractions
For rational functions P(x)/Q(x) where deg(P) < deg(Q):
- Factor Q(x) into linear and quadratic factors
- Decompose into simpler fractions
- Integrate each term

## Definite Integrals

∫ₐᵇ f(x)dx = F(b) − F(a)

### Properties
- ∫ₐᵇ f(x)dx = −∫ᵇₐ f(x)dx
- ∫ₐᵇ f(x)dx = ∫ₐᶜ f(x)dx + ∫ᶜᵇ f(x)dx
- ∫ₐᵇ f(x)dx = ∫ₐᵇ f(a+b−x)dx (King's property)
- If f is even: ∫₋ₐᵃ f(x)dx = 2∫₀ᵃ f(x)dx
- If f is odd: ∫₋ₐᵃ f(x)dx = 0

## JEE Tips

- King's property (∫₀ᵃ f(x)dx = ∫₀ᵃ f(a−x)dx) is a JEE favorite — look for symmetry.
- For ∫₀^(π/2) sinⁿ(x)dx or cosⁿ(x)dx, use Wallis' formula.
- Integration by parts with cyclic functions (eˣsin(x)): apply twice and solve the resulting equation.
