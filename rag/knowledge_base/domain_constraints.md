# Domain Constraints and Validity Checks

## Common Domain Restrictions

| Expression | Domain Restriction |
|---|---|
| 1/f(x) | f(x) ≠ 0 |
| √(f(x)) | f(x) ≥ 0 |
| log(f(x)) | f(x) > 0 |
| tan(x) | x ≠ (2n+1)π/2 |
| sin⁻¹(x), cos⁻¹(x) | −1 ≤ x ≤ 1 |
| aˣ (a > 0) | all real x |

## Range of Standard Functions

| Function | Range |
|---|---|
| sin(x), cos(x) | [−1, 1] |
| tan(x) | (−∞, ∞) |
| eˣ | (0, ∞) |
| ln(x) | (−∞, ∞) for x > 0 |
| x² | [0, ∞) |
| sin⁻¹(x) | [−π/2, π/2] |
| cos⁻¹(x) | [0, π] |
| tan⁻¹(x) | (−π/2, π/2) |

## Checking Solutions for Validity

### Extraneous Roots
When solving equations involving:
- Square roots: squaring may introduce extraneous solutions → always verify
- Logarithms: check that arguments remain positive
- Absolute values: verify each case satisfies original equation

### Division During Solution
If you divide by an expression, note the case where that expression = 0 separately.

## Units and Dimensional Analysis

- Verify that both sides of an equation have the same units/dimensions
- Angles must be consistent (radians vs degrees)
- In physics-style problems, check dimensional homogeneity

## Edge Cases to Always Check

1. **x = 0**: does the expression/function behave differently?
2. **Negative values**: is x restricted to positive?
3. **Boundary of domain**: what happens at the endpoints?
4. **Infinity behavior**: does the function approach a finite limit?
5. **Piecewise definitions**: is the function defined differently in different intervals?

## JEE Tips

- Always state the domain of the final answer.
- In "find the range" problems, set y = f(x), solve for x, then find valid y values.
- For composite functions f(g(x)), the domain is all x where g(x) is in the domain of f.
- Common trap: √(x²) = |x|, not x.
