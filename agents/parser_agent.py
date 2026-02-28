"""
Parser Agent — Converts raw input (OCR/ASR/text) into a structured math problem.
"""

import json
import re
from typing import Dict, Any, Optional

from openai import OpenAI

PARSER_SYSTEM_PROMPT = """You are a math problem parser for JEE-style questions. Your job is to:
1. Clean any OCR/ASR artifacts from the input text
2. Identify the mathematical question clearly
3. Extract structured information about the problem

Return ONLY valid JSON with this exact structure:
{
    "problem_text": "the cleaned, clearly stated math problem",
    "topic": "one of: algebra, probability, calculus, linear_algebra, trigonometry, general",
    "subtopic": "specific subtopic like 'derivatives', 'quadratic_equations', 'matrices', etc.",
    "variables": ["list", "of", "variables"],
    "constraints": ["list of constraints like 'x > 0'"],
    "needs_clarification": false,
    "clarification_reason": null
}

Rules:
- If the input is ambiguous or incomplete, set needs_clarification to true and provide a reason.
- Clean up broken symbols, extra whitespace, and OCR/ASR noise.
- Identify the core mathematical question even if poorly formatted.
- If you cannot determine the topic, use "general".
- Always extract variables used in the problem.
"""


class ParserAgent:
    """Parses raw input into a structured math problem."""

    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI()
        self.name = "Parser Agent"

    def parse(self, raw_text: str, input_type: str = "text",
              correction_rules: Dict = None) -> Dict[str, Any]:
        """
        Parse raw input text into structured problem format.

        Args:
            raw_text: The raw input from OCR, ASR, or text.
            input_type: One of 'text', 'image', 'audio'.
            correction_rules: Optional dict of correction rules to apply.

        Returns:
            Structured problem dict with trace information.
        """
        # Step 1: Apply correction rules if provided
        cleaned_text = raw_text.strip()
        if correction_rules:
            cleaned_text = self._apply_corrections(cleaned_text, input_type, correction_rules)

        # Step 2: Use LLM to parse into structured format
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": PARSER_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Parse this math problem input (from {input_type}):\n\n{cleaned_text}"},
                ],
                temperature=0,
                max_tokens=500,
            )

            result_text = response.choices[0].message.content.strip()

            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'```(?:json)?\s*(.*?)```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1).strip()

            parsed = json.loads(result_text)

        except json.JSONDecodeError:
            parsed = {
                "problem_text": cleaned_text,
                "topic": "general",
                "subtopic": "unknown",
                "variables": [],
                "constraints": [],
                "needs_clarification": True,
                "clarification_reason": "Could not automatically parse the problem structure.",
            }
        except Exception as e:
            parsed = {
                "problem_text": cleaned_text,
                "topic": "general",
                "subtopic": "unknown",
                "variables": [],
                "constraints": [],
                "needs_clarification": True,
                "clarification_reason": f"Parser error: {str(e)}",
            }

        # Step 3: Build trace
        trace = {
            "agent": self.name,
            "input": raw_text,
            "input_type": input_type,
            "cleaned_input": cleaned_text,
            "output": parsed,
        }

        return {"parsed": parsed, "trace": trace}

    def _apply_corrections(self, text: str, input_type: str, rules: Dict) -> str:
        """Apply known correction rules."""
        if input_type == "image":
            for wrong, correct in rules.get("ocr_corrections", {}).items():
                text = text.replace(wrong, correct)
        elif input_type == "audio":
            for wrong, correct in rules.get("asr_corrections", {}).items():
                # Case-insensitive replacement for ASR
                pattern = re.compile(re.escape(wrong), re.IGNORECASE)
                text = pattern.sub(correct, text)

        for rule in rules.get("learned_corrections", []):
            text = text.replace(rule["wrong"], rule["correct"])

        return text
