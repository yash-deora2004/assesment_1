"""
Router Agent — Classifies problem type and determines solution strategy.
"""

import json
import re
from typing import Dict, Any

from openai import OpenAI

ROUTER_SYSTEM_PROMPT = """You are a math problem routing agent. Given a structured math problem, you must:
1. Confirm the topic classification
2. Determine the best solution strategy

Return ONLY valid JSON:
{
    "topic": "algebra | probability | calculus | linear_algebra | trigonometry",
    "subtopic": "specific subtopic",
    "strategy": "one of: formula_application, step_by_step_derivation, numerical_computation, proof_based, mixed",
    "strategy_hint": "brief description of the recommended approach",
    "tools_needed": ["list of tools: calculator, rag, memory"],
    "difficulty": "easy | medium | hard",
    "estimated_steps": 3
}

Guidelines:
- formula_application: when a well-known formula can be directly applied
- step_by_step_derivation: when algebraic manipulation is needed
- numerical_computation: when specific numbers need to be computed (use calculator)
- proof_based: when a mathematical proof or show-that is required
- mixed: when multiple approaches are needed
- Always include "rag" in tools_needed
- Include "calculator" if numerical computation is expected
- Include "memory" if the problem seems like a common JEE type
"""


class RouterAgent:
    """Classifies problem type and routes to appropriate strategy."""

    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI()
        self.name = "Router Agent"

    def route(self, parsed_problem: Dict) -> Dict[str, Any]:
        """
        Classify and route a parsed problem.

        Args:
            parsed_problem: Structured problem from ParserAgent.

        Returns:
            Routing decision with strategy and trace.
        """
        problem_text = parsed_problem.get("problem_text", "")
        topic = parsed_problem.get("topic", "general")

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Route this problem:\n\nTopic (from parser): {topic}\nProblem: {problem_text}\nVariables: {parsed_problem.get('variables', [])}\nConstraints: {parsed_problem.get('constraints', [])}"},
                ],
                temperature=0,
                max_tokens=300,
            )

            result_text = response.choices[0].message.content.strip()

            # Extract JSON
            json_match = re.search(r'```(?:json)?\s*(.*?)```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1).strip()

            routing = json.loads(result_text)

        except (json.JSONDecodeError, Exception) as e:
            # Fallback routing
            routing = {
                "topic": topic,
                "subtopic": parsed_problem.get("subtopic", "unknown"),
                "strategy": "step_by_step_derivation",
                "strategy_hint": "Use step-by-step approach with RAG context",
                "tools_needed": ["rag", "calculator"],
                "difficulty": "medium",
                "estimated_steps": 5,
            }

        trace = {
            "agent": self.name,
            "input": parsed_problem,
            "output": routing,
        }

        return {"routing": routing, "trace": trace}
