"""
Explainer / Tutor Agent — Produces student-friendly step-by-step explanations.
"""

import json
import re
from typing import Dict, Any, List

from openai import OpenAI

EXPLAINER_SYSTEM_PROMPT = """You are a friendly and clear math tutor explaining JEE-level solutions to students.

Your job is to take a verified solution and rewrite it as a clear, step-by-step explanation that a student can follow.

Guidelines:
- Use simple, clear language
- Number each step
- Highlight key formulas in bold
- Explain WHY each step is taken, not just WHAT is done
- Add a "Common Mistake" callout if relevant (prefix with ⚠️)
- Add a "JEE Tip" if applicable (prefix with 💡)
- End with the final answer clearly stated
- If RAG sources were used, mention which formulas/concepts came from the knowledge base

Return ONLY valid JSON:
{
    "explanation": "# Solution\\n\\n**Step 1: Identify the problem type**\\n...\\n\\n**Final Answer**: x = 5",
    "key_concepts": ["Quadratic formula", "Discriminant"],
    "common_mistake": "Students often forget to consider both roots of the quadratic",
    "jee_tip": "In MCQs, check if the answer can be found faster using Vieta's formulas",
    "difficulty_rating": "medium",
    "source_references": ["algebra_equations.md"]
}

Make the explanation engaging and educational. The student should learn from reading it, not just get the answer.
"""


class ExplainerAgent:
    """Produces student-friendly explanations of solutions."""

    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI()
        self.name = "Explainer Agent"

    def explain(
        self,
        parsed_problem: Dict,
        solution: Dict,
        verification: Dict,
        rag_sources: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a student-friendly explanation.

        Args:
            parsed_problem: Structured problem.
            solution: Solution from SolverAgent.
            verification: Verification from VerifierAgent.
            rag_sources: Sources used from knowledge base.

        Returns:
            Explanation dict with trace.
        """
        problem_text = parsed_problem.get("problem_text", "")
        steps_text = self._format_steps(solution.get("steps", []))
        final_answer = solution.get("final_answer", "")

        user_prompt = f"""Create a student-friendly explanation for this solved problem:

**Problem**: {problem_text}
**Topic**: {parsed_problem.get('topic', 'general')} — {parsed_problem.get('subtopic', '')}

**Solution Steps**:
{steps_text}

**Final Answer**: {final_answer}

**Formulas Used**: {solution.get('formulas_used', [])}
**RAG Sources**: {rag_sources or []}
**Verifier Confidence**: {verification.get('confidence', 'N/A')}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": EXPLAINER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
            )

            result_text = response.choices[0].message.content.strip()

            json_match = re.search(r'```(?:json)?\s*(.*?)```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1).strip()

            explanation = json.loads(result_text)

        except json.JSONDecodeError:
            # Use the raw LLM output as the explanation
            explanation = {
                "explanation": result_text,
                "key_concepts": solution.get("formulas_used", []),
                "common_mistake": None,
                "jee_tip": None,
                "difficulty_rating": "medium",
                "source_references": rag_sources or [],
            }
        except Exception as e:
            explanation = {
                "explanation": f"**Problem**: {problem_text}\n\n**Solution**: {final_answer}\n\n(Detailed explanation unavailable: {str(e)})",
                "key_concepts": [],
                "common_mistake": None,
                "jee_tip": None,
                "difficulty_rating": "unknown",
                "source_references": [],
            }

        trace = {
            "agent": self.name,
            "input": {"problem": problem_text, "final_answer": final_answer},
            "output": {
                "has_common_mistake": bool(explanation.get("common_mistake")),
                "has_jee_tip": bool(explanation.get("jee_tip")),
                "difficulty": explanation.get("difficulty_rating", "unknown"),
            },
        }

        return {"explanation": explanation, "trace": trace}

    def _format_steps(self, steps: list) -> str:
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
