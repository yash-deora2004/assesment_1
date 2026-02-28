# Linear Algebra — Matrix Operations

## Definitions

A matrix is a rectangular array of numbers with m rows and n columns (m × n matrix).

## Types of Matrices

- **Square**: m = n
- **Identity (I)**: diagonal elements = 1, rest = 0
- **Zero matrix (O)**: all elements = 0
- **Diagonal**: non-zero only on main diagonal
- **Symmetric**: A = Aᵀ (aᵢⱼ = aⱼᵢ)
- **Skew-symmetric**: A = −Aᵀ (aᵢⱼ = −aⱼᵢ, diagonal = 0)
- **Orthogonal**: AᵀA = AAᵀ = I (i.e., A⁻¹ = Aᵀ)

## Basic Operations

- **Addition**: (A + B)ᵢⱼ = aᵢⱼ + bᵢⱼ (same dimensions required)
- **Scalar multiplication**: (kA)ᵢⱼ = k · aᵢⱼ
- **Matrix multiplication**: (AB)ᵢⱼ = Σ aᵢₖ · bₖⱼ (A is m×p, B is p×n → AB is m×n)
  - AB ≠ BA in general (not commutative)
  - A(BC) = (AB)C (associative)
  - A(B+C) = AB + AC (distributive)

## Transpose

- (Aᵀ)ᵢⱼ = aⱼᵢ
- (A + B)ᵀ = Aᵀ + Bᵀ
- (AB)ᵀ = BᵀAᵀ
- (kA)ᵀ = kAᵀ

## Inverse of a Matrix

A⁻¹ exists iff det(A) ≠ 0 (non-singular matrix).

For 2×2 matrix A = [[a, b], [c, d]]:
**A⁻¹ = (1/det(A)) · [[d, −b], [−c, a]]**

Properties:
- (A⁻¹)⁻¹ = A
- (AB)⁻¹ = B⁻¹A⁻¹
- (Aᵀ)⁻¹ = (A⁻¹)ᵀ
- det(A⁻¹) = 1/det(A)

## JEE Tips

- AB = O does NOT mean A = O or B = O.
- For 2×2 inverse, memorize the formula — faster than cofactor method.
- Any square matrix can be written as sum of symmetric and skew-symmetric: A = (A + Aᵀ)/2 + (A − Aᵀ)/2.
