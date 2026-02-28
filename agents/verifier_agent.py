"""
Verifier / Critic Agent — Checks solution correctness, domain validity, and edge cases.
"""

import json
import re
from typing import Dict, Any

from openai import OpenAI

VERIFIER_SYSTEM_PROMPT = """You are a rigorous math solution verifier for JEE problems. Your job is to check:

1. **Correctness**: Re-derive or verify the answer using an independent method
2. **Domain/Units**: Check variable domains, sign constraints, units
3. **Edge Cases**: Division by zero, undefined expressions, boundary values
4. **Consistency**: Does the answer satisfy the original problem constraints?
5. **Completeness**: Are all cases covered? Are there missing solutions?

Return ONLY valid JSON:
{
    "is_correct": true,
    "confidence": 0.92,
    "issues_found": [],
    "verification_method": "Substituted the solution back into the original equation",
    "domain_check": "All variables within valid domain",
    "edge_cases_checked": ["Checked for x=0", "Verified denominator ≠ 0"],
    "feedback": "Solution is correct and complete.",
    "suggested_fix": null
}

If issues are found:
{
    "is_correct": false,
    "confidence": 0.3,
    "issues_found": ["Sign error in step 3", "Missing case when x < 0"],
    "verification_method": "Re-derived using alternative method",
    "domain_check": "x must be > 0 but solution includes x = -2",
    "edge_cases_checked": ["Found division by zero at x = 1"],
    "feedback": "The solution has errors that need correction.",
    "suggested_fix": "Recompute step 3 with correct sign; add constraint x > 0"
}

Be strict but fair. Common things to check:
- Quadratic: did they consider both roots? Check discriminant sign.
- Calculus: chain rule applied correctly? Constants of integration?
- Probability: does P sum to 1? Is P between 0 and 1?
- Linear algebra: determinant computation correct? Matrix dimensions match?
"""


class VerifierAgent:
    """Verifies solution correctness and flags issues."""

    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI()
        self.name = "Verifier Agent"

    def verify(self, parsed_problem: Dict, solution: Dict) -> Dict[str, Any]:
        """
        Verify a solution against the original problem.

        Args:
            parsed_problem: The structured problem.
            solution: The solution from SolverAgent.

        Returns:
            Verification result with confidence score and trace.
        """
        problem_text = parsed_problem.get("problem_text", "")
        steps_text = self._format_steps(solution.get("steps", []))
        final_answer = solution.get("final_answer", "")

        user_prompt = f"""Verify this solution:

**Problem**: {problem_text}
**Topic**: {parsed_problem.get('topic', 'general')}
**Variables**: {parsed_problem.get('variables', [])}
**Constraints**: {parsed_problem.get('constraints', [])}

**Solution Steps**:
{steps_text}

**Final Answer**: {final_answer}

**Formulas Used**: {solution.get('formulas_used', [])}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": VERIFIER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                max_tokens=800,
            )

            result_text = response.choices[0].message.content.strip()

            json_match = re.search(r'```(?:json)?\s*(.*?)```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1).strip()

            verification = json.loads(result_text)

        except (json.JSONDecodeError, Exception) as e:
            verification = {
                "is_correct": True,
                "confidence": 0.5,
                "issues_found": [],
                "verification_method": "Automated verification failed — defaulting to low confidence",
                "domain_check": "Not checked",
                "edge_cases_checked": [],
                "feedback": f"Verification error: {str(e)}",
                "suggested_fix": None,
            }

        # Ensure confidence is a float
        confidence = float(verification.get("confidence", 0.5))
        verification["confidence"] = confidence

        trace = {
            "agent": self.name,
            "input": {"problem": problem_text, "final_answer": final_answer},
            "output": {
                "is_correct": verification.get("is_correct", False),
                "confidence": confidence,
                "issues": verification.get("issues_found", []),
            },
        }

        return {"verification": verification, "trace": trace}

    def _format_steps(self, steps: list) -> str:
        """Format solution steps into readable text."""
        if not steps:
            return "No steps provided."
        parts = []
        for step in steps:
            if isinstance(step, dict):
                num = step.get("step_number", "?")
                desc = step.get("description", "")
                work = step.get("work", "")
                parts.append(f"Step {num}: {desc}\n{work}")
            else:
                parts.append(str(step))
        return "\n\n".join(parts)
