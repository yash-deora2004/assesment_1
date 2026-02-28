# Linear Algebra — Vectors

## Basics

A vector **v** = aî + bĵ + ck̂ in 3D space.
- Magnitude: |**v**| = √(a² + b² + c²)
- Unit vector: v̂ = **v** / |**v**|

## Vector Operations

- **Addition**: (a₁, b₁, c₁) + (a₂, b₂, c₂) = (a₁+a₂, b₁+b₂, c₁+c₂)
- **Scalar multiplication**: k(a, b, c) = (ka, kb, kc)

## Dot Product (Scalar Product)

**a · b** = a₁b₁ + a₂b₂ + a₃b₃ = |**a**||**b**|cos(θ)

Properties:
- **a · b** = 0 ⟺ **a** ⊥ **b** (perpendicular)
- **a · a** = |**a**|²
- Commutative: **a · b** = **b · a**
- Distributive: **a · (b + c)** = **a · b** + **a · c**

## Cross Product (Vector Product)

**a × b** = |î  ĵ  k̂; a₁ a₂ a₃; b₁ b₂ b₃| (determinant form)

= (a₂b₃ − a₃b₂)î − (a₁b₃ − a₃b₁)ĵ + (a₁b₂ − a₂b₁)k̂

Properties:
- |**a × b**| = |**a**||**b**|sin(θ) = area of parallelogram
- **a × b** = −(**b × a**) (anti-commutative)
- **a × a** = **0**
- **a × b** = **0** ⟺ **a** ∥ **b** (parallel)

## Scalar Triple Product

**a · (b × c)** = det([a₁ a₂ a₃; b₁ b₂ b₃; c₁ c₂ c₃])

- |**a · (b × c)**| = volume of parallelepiped
- If **a · (b × c)** = 0, the vectors are coplanar

## Projection

- Projection of **a** on **b**: proj = (**a · b** / |**b**|²) · **b**
- Scalar projection: **a · b** / |**b**|

## JEE Tips

- For "find a vector perpendicular to both **a** and **b**", compute **a × b**.
- Volume of tetrahedron = (1/6)|**a · (b × c)**|.
- If three vectors are coplanar, their scalar triple product = 0.
- Component of **a** along **b** = (**a · b**)/|**b**| (scalar); projection vector = [(**a · b**)/|**b**|²]**b**.
