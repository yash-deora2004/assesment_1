# Linear Algebra — Determinants

## 2×2 Determinant

det([[a, b], [c, d]]) = ad − bc

## 3×3 Determinant (Cofactor Expansion)

det(A) = a₁₁(a₂₂a₃₃ − a₂₃a₃₂) − a₁₂(a₂₁a₃₃ − a₂₃a₃₁) + a₁₃(a₂₁a₃₂ − a₂₂a₃₁)

(Expansion along first row; can expand along any row or column.)

## Properties of Determinants

1. det(Aᵀ) = det(A)
2. Swapping two rows (or columns) changes the sign of det
3. If two rows (or columns) are identical, det = 0
4. Multiplying a row by k multiplies det by k
5. det(kA) = kⁿ · det(A) for n×n matrix
6. **det(AB) = det(A) · det(B)**
7. det(A⁻¹) = 1/det(A)
8. Adding a multiple of one row to another doesn't change det
9. If a row (or column) is all zeros, det = 0

## Cofactor and Adjoint

- **Minor** Mᵢⱼ: determinant of submatrix obtained by deleting row i and column j
- **Cofactor** Cᵢⱼ = (−1)^(i+j) · Mᵢⱼ
- **Adjoint**: adj(A) = transpose of cofactor matrix
- **A⁻¹ = adj(A) / det(A)**
- A · adj(A) = det(A) · I

## Cramer's Rule

For system AX = B where A is n×n and det(A) ≠ 0:
- xᵢ = det(Aᵢ) / det(A)
- where Aᵢ is A with column i replaced by B

## Special Determinants

- **Vandermonde**: det of [[1, a, a²], [1, b, b²], [1, c, c²]] = (b−a)(c−a)(c−b)
- Diagonal matrix: det = product of diagonal elements
- Triangular matrix: det = product of diagonal elements

## JEE Tips

- Use row/column operations to simplify before expanding.
- det(adj(A)) = det(A)^(n−1) for n×n matrix.
- If det(A) = 0, the system AX = B either has no solution or infinitely many.
