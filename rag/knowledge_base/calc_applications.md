# Calculus — Applications (Maxima, Minima, Rate of Change)

## Rate of Change

- **Instantaneous rate of change** of y = f(x) at x = a is f'(a)
- If s(t) = position, then v(t) = s'(t) = velocity, a(t) = v'(t) = s''(t) = acceleration

## Increasing and Decreasing Functions

- f is **increasing** on interval I if f'(x) > 0 for all x in I
- f is **decreasing** on interval I if f'(x) < 0 for all x in I

## Maxima and Minima

### First Derivative Test
1. Find critical points: f'(x) = 0 or f'(x) undefined
2. Check sign of f'(x) around each critical point:
   - f' changes from + to − → local maximum
   - f' changes from − to + → local minimum
   - f' doesn't change sign → neither (inflection point)

### Second Derivative Test
At critical point x = c where f'(c) = 0:
- f''(c) > 0 → local minimum
- f''(c) < 0 → local maximum
- f''(c) = 0 → test is inconclusive, use first derivative test

### Absolute (Global) Extrema on [a, b]
1. Find all critical points in (a, b)
2. Evaluate f at each critical point and at endpoints a, b
3. Largest value = absolute max, smallest = absolute min

## Optimization Problems

1. Identify the quantity to optimize
2. Express it as a function of one variable
3. Find the domain (constraints)
4. Use derivative tests to find max/min
5. Verify the answer makes sense in context

## Tangent and Normal Lines

- **Tangent** at (a, f(a)): y − f(a) = f'(a)(x − a)
- **Normal** at (a, f(a)): y − f(a) = −1/f'(a) · (x − a)
- Angle between two curves: tan(θ) = |(m₁ − m₂)/(1 + m₁m₂)|

## JEE Tips

- For "find the minimum value of f(x) for x > 0", always check endpoints and behavior at 0⁺ and ∞.
- Many optimization problems reduce to AM-GM — check before using calculus.
- For problems asking "find the point on curve closest to a point", minimize distance² (avoids square root).
