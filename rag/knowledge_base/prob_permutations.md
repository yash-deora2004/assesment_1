# Probability — Permutations and Combinations

## Fundamental Counting Principle

If task 1 can be done in m ways and task 2 in n ways, then both together: m × n ways.

## Permutations (Order Matters)

- **P(n, r) = n! / (n−r)!** — arrangements of r objects from n distinct objects
- **Permutations of n objects**: n!
- **With repetition**: n objects where p are identical of type 1, q identical of type 2, etc.: n! / (p! · q! · ...)
- **Circular permutations**: (n−1)! for n objects in a circle

## Combinations (Order Doesn't Matter)

- **C(n, r) = n! / (r! · (n−r)!)**
- C(n, 0) = C(n, n) = 1
- C(n, r) = C(n, n−r)
- C(n, r) + C(n, r−1) = C(n+1, r) (Pascal's identity)

## Useful Identities

- Σ C(n, k) for k = 0 to n = 2ⁿ
- C(n, 0) − C(n, 1) + C(n, 2) − ... = 0
- C(n, 1) + C(n, 2) + ... + C(n, n) = 2ⁿ − 1

## Common Problem Types

### Distribution of Identical Objects
- Distributing n identical objects into r distinct groups: C(n+r−1, r−1) (stars and bars)

### Derangements
- Number of permutations with no element in original position:
  D(n) = n! · Σ (−1)^k / k! for k = 0 to n

### Multinomial Coefficient
- Ways to divide n objects into groups of sizes k₁, k₂, ..., kᵣ:
  n! / (k₁! · k₂! · ... · kᵣ!)

## JEE Tips

- "Select" → combination; "arrange" → permutation.
- For "at least one" selection: total selections − selections with none = 2ⁿ − 1.
- Stars and bars is the go-to technique for distribution problems.
- For problems with restrictions, count total − restricted.
