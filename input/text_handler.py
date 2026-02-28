"""
Text Input Handler — Processes direct text input.
"""

from typing import Dict, Any


class TextHandler:
    """Handles direct text input from the user."""

    def __init__(self):
        self.name = "Text Handler"

    def process(self, text: str) -> Dict[str, Any]:
        """
        Process text input.

        Args:
            text: Raw text input from user.

        Returns:
            Dict with extracted text and metadata.
        """
        cleaned = text.strip()

        return {
            "text": cleaned,
            "input_type": "text",
            "confidence": 1.0,  # Direct text is always high confidence
            "needs_review": False,
            "raw_input": text,
        }
