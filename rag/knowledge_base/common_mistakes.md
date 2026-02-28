# Common Mistakes in JEE Mathematics

## Algebra

1. **Incorrect expansion**: (a + b)² ≠ a² + b². Must include 2ab term.
2. **Division by zero**: when dividing both sides by an expression, ensure it's non-zero.
3. **Log domain errors**: log(x) requires x > 0. Students forget to check domain.
4. **Square root assumption**: √(x²) = |x|, NOT x. For x < 0, √(x²) = −x.
5. **Quadratic roots**: forgetting to check discriminant before claiming roots are real.
6. **Modulus errors**: |a + b| ≠ |a| + |b| in general. Only |a · b| = |a| · |b|.

## Calculus

7. **Chain rule omission**: d/dx[sin(2x)] = 2cos(2x), NOT cos(2x).
8. **Integration constant**: forgetting +C in indefinite integrals.
9. **L'Hôpital misuse**: applying L'Hôpital when the form is NOT 0/0 or ∞/∞.
10. **Derivative of constant**: treating a parameter as a variable when differentiating.
11. **Product rule neglect**: d/dx[x·eˣ] = eˣ + xeˣ, NOT xeˣ.
12. **Limits at infinity**: lim(x→∞) sin(x)/x = 0 (squeeze theorem), NOT "doesn't exist".

## Probability

13. **Confusing P(A|B) with P(B|A)**: conditional probability is not symmetric.
14. **Assuming independence**: events are independent only if P(A∩B) = P(A)·P(B).
15. **Overcounting**: in combinatorics, distinguishing between ordered/unordered selections.
16. **Forgetting complement**: "at least one" is easier as 1 − P(none).

## Linear Algebra

17. **Matrix multiplication order**: AB ≠ BA in general.
18. **Determinant of sum**: det(A + B) ≠ det(A) + det(B).
19. **Inverse assumptions**: not all square matrices are invertible.
20. **Row operations in determinants**: adding rows is fine, but multiplying changes the determinant.

## General

21. **Unit mismatch**: mixing radians and degrees.
22. **Sign errors**: the #1 source of wrong answers — track negative signs carefully.
23. **Not checking answers**: always substitute back to verify, especially in equations with potential extraneous roots.
24. **Incomplete case analysis**: forgetting edge cases like x = 0, or sign of denominator.
