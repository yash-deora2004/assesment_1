"""Tests for the Memory Store and HITL modules."""

import unittest
import os
import tempfile
import json

from hitl.review import HITLManager, HITLAction, HITLTrigger, HITLRequest


class TestHITLManager(unittest.TestCase):
    """Test cases for the HITL manager."""

    def setUp(self):
        self.manager = HITLManager()

    def test_check_ocr_low_confidence(self):
        """Test that low OCR confidence triggers HITL."""
        request = self.manager.check_ocr_confidence(50.0, "some text")
        self.assertIsNotNone(request)
        self.assertEqual(request.trigger, HITLTrigger.LOW_OCR_CONFIDENCE)
        self.assertTrue(self.manager.has_pending_reviews())

    def test_check_ocr_high_confidence(self):
        """Test that high OCR confidence does not trigger HITL."""
        request = self.manager.check_ocr_confidence(90.0, "some text")
        self.assertIsNone(request)
        self.assertFalse(self.manager.has_pending_reviews())

    def test_check_asr_low_confidence(self):
        """Test that low ASR confidence triggers HITL."""
        request = self.manager.check_asr_confidence(0.3, "some text")
        self.assertIsNotNone(request)
        self.assertEqual(request.trigger, HITLTrigger.LOW_ASR_CONFIDENCE)

    def test_check_parser_ambiguity(self):
        """Test that parser ambiguity triggers HITL."""
        parsed = {"needs_clarification": True, "clarification_reason": "Ambiguous variables"}
        request = self.manager.check_parser_ambiguity(parsed)
        self.assertIsNotNone(request)
        self.assertEqual(request.trigger, HITLTrigger.PARSER_AMBIGUITY)

    def test_check_parser_no_ambiguity(self):
        """Test that clear parsing does not trigger HITL."""
        parsed = {"needs_clarification": False}
        request = self.manager.check_parser_ambiguity(parsed)
        self.assertIsNone(request)

    def test_check_verifier_low_confidence(self):
        """Test that low verifier confidence triggers HITL."""
        request = self.manager.check_verifier_confidence(0.4, "x = 5", "solve x")
        self.assertIsNotNone(request)
        self.assertEqual(request.trigger, HITLTrigger.LOW_VERIFIER_CONFIDENCE)

    def test_resolve_approve(self):
        """Test approving a review."""
        request = HITLRequest(
            trigger=HITLTrigger.LOW_OCR_CONFIDENCE,
            reason="Low confidence",
            current_data={"text": "original"},
            agent_source="image_handler",
        )
        self.manager.pending_reviews.append(request)

        result = self.manager.resolve_review(request, HITLAction.APPROVE)
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["data"]["text"], "original")
        self.assertFalse(self.manager.has_pending_reviews())

    def test_resolve_edit(self):
        """Test editing in a review."""
        request = HITLRequest(
            trigger=HITLTrigger.LOW_OCR_CONFIDENCE,
            reason="Low confidence",
            current_data={"text": "original"},
            agent_source="image_handler",
        )
        self.manager.pending_reviews.append(request)

        result = self.manager.resolve_review(
            request, HITLAction.EDIT, edited_data={"text": "edited"}
        )
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["data"]["text"], "edited")

    def test_resolve_reject(self):
        """Test rejecting a review."""
        request = HITLRequest(
            trigger=HITLTrigger.LOW_OCR_CONFIDENCE,
            reason="Low confidence",
            current_data={"text": "original"},
            agent_source="image_handler",
        )
        self.manager.pending_reviews.append(request)

        result = self.manager.resolve_review(request, HITLAction.REJECT, comment="bad input")
        self.assertEqual(result["action"], "retry")

    def test_review_summary(self):
        """Test review summary."""
        self.manager.check_ocr_confidence(50.0, "text")
        summary = self.manager.get_review_summary()
        self.assertEqual(summary["pending"], 1)
        self.assertEqual(summary["completed"], 0)


class TestCorrectionRules(unittest.TestCase):
    """Test correction rules loading."""

    def test_correction_rules_file_exists(self):
        """Test that correction_rules.json exists."""
        path = os.path.join(os.path.dirname(__file__), "..", "memory", "correction_rules.json")
        self.assertTrue(os.path.exists(path))

    def test_correction_rules_structure(self):
        """Test correction rules JSON structure."""
        path = os.path.join(os.path.dirname(__file__), "..", "memory", "correction_rules.json")
        with open(path, encoding="utf-8") as f:
            rules = json.load(f)
        self.assertIn("ocr_corrections", rules)
        self.assertIn("asr_corrections", rules)
        self.assertIn("learned_corrections", rules)


if __name__ == "__main__":
    unittest.main()
