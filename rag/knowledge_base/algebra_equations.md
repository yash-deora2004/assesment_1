# Algebra — Solving Equations

## Quadratic Equations

**Standard form**: ax² + bx + c = 0

- **Quadratic formula**: x = (−b ± √(b² − 4ac)) / 2a
- **Discriminant (D)** = b² − 4ac
  - D > 0 → two distinct real roots
  - D = 0 → one repeated real root
  - D < 0 → two complex conjugate roots

### Vieta's Formulas (Quadratic)
For roots α, β of ax² + bx + c = 0:
- α + β = −b/a
- αβ = c/a

## Cubic Equations

**Standard form**: ax³ + bx² + cx + d = 0

### Vieta's Formulas (Cubic)
For roots α, β, γ:
- α + β + γ = −b/a
- αβ + βγ + γα = c/a
- αβγ = −d/a

### Nature of Roots
- Use the discriminant Δ = 18abcd − 4b³d + b²c² − 4ac³ − 27a²d²
- Δ > 0 → three distinct real roots
- Δ = 0 → repeated root(s)
- Δ < 0 → one real root + two complex conjugate roots

## Systems of Equations

- **Substitution**: isolate one variable, substitute into other equation(s)
- **Elimination**: multiply equations to cancel one variable
- **Cramer's Rule**: x = Dₓ/D, y = Dᵧ/D (see Linear Algebra — Determinants)

## JEE Tips

- For "find the condition that roots are equal", set D = 0.
- If roots are reciprocal of each other, then c = a.
- If one root is k times the other, use Vieta's to set up the relation.
- For equations reducible to quadratic, try substitution (e.g., let t = x²).
