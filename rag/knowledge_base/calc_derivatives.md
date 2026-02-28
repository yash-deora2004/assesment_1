# Calculus — Differentiation Rules and Formulas

## Definition

f'(x) = lim(h→0) [f(x+h) − f(x)] / h

## Basic Derivative Rules

1. **Constant**: d/dx [c] = 0
2. **Power rule**: d/dx [xⁿ] = nxⁿ⁻¹
3. **Sum rule**: d/dx [f + g] = f' + g'
4. **Product rule**: d/dx [f·g] = f'g + fg'
5. **Quotient rule**: d/dx [f/g] = (f'g − fg') / g²
6. **Chain rule**: d/dx [f(g(x))] = f'(g(x)) · g'(x)

## Standard Derivatives

| Function | Derivative |
|---|---|
| sin(x) | cos(x) |
| cos(x) | −sin(x) |
| tan(x) | sec²(x) |
| cot(x) | −csc²(x) |
| sec(x) | sec(x)tan(x) |
| csc(x) | −csc(x)cot(x) |
| eˣ | eˣ |
| aˣ | aˣ · ln(a) |
| ln(x) | 1/x |
| log_a(x) | 1/(x·ln(a)) |
| sin⁻¹(x) | 1/√(1−x²) |
| cos⁻¹(x) | −1/√(1−x²) |
| tan⁻¹(x) | 1/(1+x²) |

## Logarithmic Differentiation

For functions of the form y = f(x)^g(x):
1. Take ln of both sides: ln(y) = g(x) · ln(f(x))
2. Differentiate both sides
3. Solve for dy/dx

## Implicit Differentiation

When y is defined implicitly by F(x, y) = 0:
- Differentiate both sides with respect to x
- Treat y as a function of x (use chain rule: d/dx[f(y)] = f'(y) · dy/dx)
- Solve for dy/dx

## Higher Order Derivatives

- Second derivative: f''(x) = d²y/dx²
- nth derivative: f⁽ⁿ⁾(x) = dⁿy/dxⁿ

## JEE Tips

- Chain rule is used in nearly every derivative problem — master it.
- For parametric equations x = f(t), y = g(t): dy/dx = (dy/dt)/(dx/dt).
- Logarithmic differentiation is essential for products of many functions.
