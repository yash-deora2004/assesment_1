# Probability — Basics

## Definitions

- **Experiment**: a process with uncertain outcomes (e.g., rolling a die)
- **Sample Space (S)**: set of all possible outcomes
- **Event (E)**: a subset of the sample space
- **P(E)** = number of favorable outcomes / total outcomes (for equally likely outcomes)

## Axioms of Probability

1. 0 ≤ P(E) ≤ 1 for any event E
2. P(S) = 1
3. For mutually exclusive events E₁, E₂, ...: P(E₁ ∪ E₂ ∪ ...) = P(E₁) + P(E₂) + ...

## Basic Rules

- **Complement**: P(E') = 1 − P(E)
- **Addition Rule**: P(A ∪ B) = P(A) + P(B) − P(A ∩ B)
- **For mutually exclusive events**: P(A ∪ B) = P(A) + P(B)
- **Inclusion-Exclusion** (3 events):
  P(A ∪ B ∪ C) = P(A) + P(B) + P(C) − P(A∩B) − P(B∩C) − P(A∩C) + P(A∩B∩C)

## Types of Events

- **Mutually exclusive**: A ∩ B = ∅ (cannot occur simultaneously)
- **Exhaustive**: A ∪ B = S (cover the entire sample space)
- **Independent**: P(A ∩ B) = P(A) · P(B)

## Classical Problems

- **Dice**: P(sum = 7 with two dice) = 6/36 = 1/6
- **Cards**: P(drawing an ace) = 4/52 = 1/13
- **Coins**: P(at least one head in n tosses) = 1 − (1/2)ⁿ

## JEE Tips

- "At least one" problems: use complement. P(at least 1) = 1 − P(none).
- Always verify your sample space size before computing probability.
- Distinguish between "with replacement" and "without replacement".
