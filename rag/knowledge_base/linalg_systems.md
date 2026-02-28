# Linear Algebra — Solving Systems of Equations

## Representation

A system of linear equations can be written as AX = B:
- A = coefficient matrix
- X = variable vector
- B = constant vector

## Methods of Solving

### 1. Cramer's Rule (for unique solutions)
If det(A) ≠ 0:
- xᵢ = det(Aᵢ) / det(A)
- Aᵢ = A with column i replaced by B

### 2. Inverse Method
If A⁻¹ exists: X = A⁻¹B

### 3. Gaussian Elimination
Reduce augmented matrix [A|B] to row echelon form using row operations.

## Nature of Solutions

### Homogeneous System (AX = 0)
- Always has trivial solution X = 0
- Non-trivial solutions exist iff det(A) = 0
- If n unknowns and rank(A) = r < n → infinite solutions with (n−r) free variables

### Non-Homogeneous System (AX = B)
- **det(A) ≠ 0** → unique solution (consistent)
- **det(A) = 0**:
  - If adj(A)·B = 0 → infinitely many solutions
  - If adj(A)·B ≠ 0 → no solution (inconsistent)

## Rank of a Matrix

- Rank = number of non-zero rows in row echelon form
- rank(A) ≤ min(m, n)
- System is consistent iff rank(A) = rank([A|B])
- Unique solution: rank(A) = rank([A|B]) = n (number of unknowns)
- Infinite solutions: rank(A) = rank([A|B]) < n

## 2-Variable System (Geometric Interpretation)

- Unique solution → two lines intersect at one point
- No solution → parallel lines (inconsistent)
- Infinite solutions → same line (dependent)

## 3-Variable System

- Unique solution → three planes meet at a point
- No solution → planes don't have a common intersection
- Infinite solutions → planes intersect along a line or coincide

## JEE Tips

- For 3×3 systems, compute det(A) first. If non-zero, use Cramer's rule.
- "Find the condition for consistency" usually means: find when det(A) = 0 AND adj(A)·B = 0.
- For homogeneous systems, "non-trivial solution exists" ⟺ det(A) = 0.
