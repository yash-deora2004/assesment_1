# Probability — Conditional Probability & Bayes' Theorem

## Conditional Probability

**P(A|B) = P(A ∩ B) / P(B)**, where P(B) > 0

Interpretation: probability of A occurring given that B has occurred.

## Multiplication Rule

P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A)

For independent events: P(A ∩ B) = P(A) · P(B)

## Total Probability Theorem

If B₁, B₂, ..., Bₙ are mutually exclusive and exhaustive events:

**P(A) = Σ P(A|Bᵢ) · P(Bᵢ)**

## Bayes' Theorem

**P(Bⱼ|A) = P(A|Bⱼ) · P(Bⱼ) / Σ P(A|Bᵢ) · P(Bᵢ)**

### Interpretation
- P(Bⱼ) = prior probability of hypothesis Bⱼ
- P(A|Bⱼ) = likelihood of evidence A given Bⱼ
- P(Bⱼ|A) = posterior probability of Bⱼ after observing A

## Classic Problems

### Urn Problems
- Urn 1 has 3 red, 2 blue. Urn 2 has 1 red, 4 blue.
- Select an urn at random, draw a ball.
- If the ball is red, find P(it came from Urn 1) → use Bayes'.

### Medical Testing
- Disease prevalence: P(D) = 0.01
- Test sensitivity: P(+|D) = 0.99
- Test specificity: P(−|D') = 0.95
- P(D|+) = P(+|D)·P(D) / [P(+|D)·P(D) + P(+|D')·P(D')]

## JEE Tips

- Draw a tree diagram for conditional probability problems.
- Bayes' theorem is the "reverse" of total probability — it updates prior beliefs.
- Check independence: events are independent iff P(A ∩ B) = P(A) · P(B).
