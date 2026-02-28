"""Tests for the Parser Agent."""

import unittest
from unittest.mock import MagicMock, patch
import json


class TestParserAgent(unittest.TestCase):
    """Test cases for ParserAgent."""

    def test_apply_corrections_ocr(self):
        """Test OCR correction rules are applied."""
        from agents.parser_agent import ParserAgent

        agent = ParserAgent(client=MagicMock())
        rules = {
            "ocr_corrections": {"teh": "the"},
            "asr_corrections": {},
            "learned_corrections": [],
        }
        result = agent._apply_corrections("Solve teh equation", "image", rules)
        self.assertEqual(result, "Solve the equation")

    def test_apply_corrections_audio(self):
        """Test ASR correction rules are applied."""
        from agents.parser_agent import ParserAgent

        agent = ParserAgent(client=MagicMock())
        rules = {
            "ocr_corrections": {},
            "asr_corrections": {"square root of x": "√x"},
            "learned_corrections": [],
        }
        result = agent._apply_corrections("find the square root of x", "audio", rules)
        self.assertIn("√x", result)

    def test_apply_learned_corrections(self):
        """Test learned correction rules are applied."""
        from agents.parser_agent import ParserAgent

        agent = ParserAgent(client=MagicMock())
        rules = {
            "ocr_corrections": {},
            "asr_corrections": {},
            "learned_corrections": [{"wrong": "derivtive", "correct": "derivative"}],
        }
        result = agent._apply_corrections("find the derivtive", "text", rules)
        self.assertEqual(result, "find the derivative")


class TestParserAgentParse(unittest.TestCase):
    """Test full parse method with mocked LLM."""

    @patch("agents.parser_agent.ParserAgent.__init__", return_value=None)
    def test_parse_returns_structure(self, mock_init):
        """Test that parse returns expected structure."""
        from agents.parser_agent import ParserAgent

        agent = ParserAgent.__new__(ParserAgent)
        agent.name = "Parser Agent"

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps({
            "problem_text": "Find x if 2x + 3 = 7",
            "topic": "algebra",
            "subtopic": "linear_equations",
            "variables": ["x"],
            "constraints": [],
            "needs_clarification": False,
            "clarification_reason": None,
        })
        mock_client.chat.completions.create.return_value = mock_response
        agent.client = mock_client

        result = agent.parse("Find x if 2x + 3 = 7")
        self.assertIn("parsed", result)
        self.assertIn("trace", result)
        self.assertEqual(result["parsed"]["topic"], "algebra")


if __name__ == "__main__":
    unittest.main()
