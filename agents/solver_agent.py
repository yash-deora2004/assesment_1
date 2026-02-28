"""
Solver Agent — Solves math problems using RAG context + optional calculator tool.
"""

import json
import re
from typing import Dict, Any, List, Optional

from openai import OpenAI

from tools.calculator import run_calculation

SOLVER_SYSTEM_PROMPT = """You are an expert JEE math problem solver. You must solve the given problem step-by-step.

You have access to:
1. **Retrieved Knowledge Context** — relevant formulas and templates from the knowledge base
2. **Calculator Tool** — for numerical computations (you'll be told results)
3. **Similar Past Problems** — solutions to similar problems from memory

Instructions:
- Solve the problem completely with clear intermediate steps
- Reference which formulas or knowledge you're using
- Show all work — do not skip steps
- If the retrieved context contains relevant formulas, cite the source
- If you need a calculation, describe what needs to be computed
- End with a clear, boxed final answer

Format your response as JSON:
{
    "steps": [
        {"step_number": 1, "description": "Identify the problem type", "work": "This is a quadratic equation..."},
        {"step_number": 2, "description": "Apply the formula", "work": "Using x = (-b ± √(b²-4ac)) / 2a..."}
    ],
    "final_answer": "x = 3 or x = -2",
    "formulas_used": ["Quadratic formula", "Vieta's formulas"],
    "rag_sources_cited": ["algebra_equations.md"],
    "calculator_used": false,
    "confidence_hint": 0.9
}
"""


class SolverAgent:
    """Solves math problems using RAG context and tools."""

    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI()
        self.name = "Solver Agent"

    def solve(
        self,
        parsed_problem: Dict,
        routing: Dict,
        rag_context: str,
        rag_sources: List[str] = None,
        similar_problems: List[Dict] = None,
        verifier_feedback: str = None,
    ) -> Dict[str, Any]:
        """
        Solve a math problem with RAG context.

        Args:
            parsed_problem: Structured problem from ParserAgent.
            routing: Routing decision from RouterAgent.
            rag_context: Formatted context string from RAG retriever.
            rag_sources: List of source files used.
            similar_problems: Similar past problems from memory.
            verifier_feedback: Feedback from verifier if this is a retry.

        Returns:
            Solution dict with steps and trace.
        """
        problem_text = parsed_problem.get("problem_text", "")
        strategy = routing.get("strategy", "step_by_step_derivation")
        strategy_hint = routing.get("strategy_hint", "")

        # Build the prompt
        user_prompt = f"""Solve this problem:

**Problem**: {problem_text}

**Topic**: {routing.get('topic', 'general')} — {routing.get('subtopic', '')}
**Strategy**: {strategy} — {strategy_hint}
**Variables**: {parsed_problem.get('variables', [])}
**Constraints**: {parsed_problem.get('constraints', [])}

**Retrieved Knowledge Context**:
{rag_context}
"""

        if similar_problems:
            user_prompt += "\n**Similar Past Problems (from memory)**:\n"
            for sp in similar_problems[:2]:
                prev_problem = sp.get("parsed_problem", {})
                if isinstance(prev_problem, dict):
                    prev_text = prev_problem.get("problem_text", "N/A")
                else:
                    prev_text = str(prev_problem)
                user_prompt += f"- Previous: {prev_text}\n  Solution approach: {sp.get('solution', 'N/A')[:200]}\n"

        if verifier_feedback:
            user_prompt += f"\n**IMPORTANT — Verifier Feedback (fix these issues)**:\n{verifier_feedback}\n"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SOLVER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=2000,
            )

            result_text = response.choices[0].message.content.strip()

            # Extract JSON
            json_match = re.search(r'```(?:json)?\s*(.*?)```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1).strip()

            solution = json.loads(result_text)

        except json.JSONDecodeError:
            # If JSON parsing fails, treat the whole response as the solution
            solution = {
                "steps": [{"step_number": 1, "description": "Solution", "work": result_text}],
                "final_answer": result_text.split("answer")[-1].strip() if "answer" in result_text.lower() else result_text[-200:],
                "formulas_used": [],
                "rag_sources_cited": rag_sources or [],
                "calculator_used": False,
                "confidence_hint": 0.6,
            }
        except Exception as e:
            solution = {
                "steps": [{"step_number": 1, "description": "Error", "work": f"Solver encountered an error: {str(e)}"}],
                "final_answer": "Error — could not solve",
                "formulas_used": [],
                "rag_sources_cited": [],
                "calculator_used": False,
                "confidence_hint": 0.0,
            }

        # Ensure rag_sources_cited reflects actual sources
        if rag_sources and not solution.get("rag_sources_cited"):
            solution["rag_sources_cited"] = rag_sources

        trace = {
            "agent": self.name,
            "input": {
                "problem": problem_text,
                "strategy": strategy,
                "rag_sources": rag_sources,
                "had_similar_problems": bool(similar_problems),
                "is_retry": bool(verifier_feedback),
            },
            "output": {
                "num_steps": len(solution.get("steps", [])),
                "final_answer": solution.get("final_answer", ""),
                "confidence_hint": solution.get("confidence_hint", 0),
            },
        }

        return {"solution": solution, "trace": trace}
