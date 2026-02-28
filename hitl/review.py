"""
Human-in-the-Loop — Trigger logic and review state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List


class HITLAction(Enum):
    APPROVE = "approve"
    EDIT = "edit"
    REJECT = "reject"


class HITLTrigger(Enum):
    LOW_OCR_CONFIDENCE = "low_ocr_confidence"
    LOW_ASR_CONFIDENCE = "low_asr_confidence"
    PARSER_AMBIGUITY = "parser_ambiguity"
    LOW_VERIFIER_CONFIDENCE = "low_verifier_confidence"
    USER_INITIATED = "user_initiated"


# Thresholds
OCR_CONFIDENCE_THRESHOLD = 70.0
ASR_CONFIDENCE_THRESHOLD = 0.6
VERIFIER_CONFIDENCE_THRESHOLD = 0.7


@dataclass
class HITLRequest:
    """Represents a pending HITL review request."""
    trigger: HITLTrigger
    reason: str
    current_data: Dict[str, Any]
    agent_source: str
    resolved: bool = False
    action: Optional[HITLAction] = None
    edited_data: Optional[Dict[str, Any]] = None
    feedback_comment: Optional[str] = None


class HITLManager:
    """Manages HITL review requests and responses."""

    def __init__(self):
        self.pending_reviews: List[HITLRequest] = []
        self.review_history: List[HITLRequest] = []

    def check_ocr_confidence(self, confidence: float, extracted_text: str) -> Optional[HITLRequest]:
        """Check if OCR output needs human review."""
        if confidence < OCR_CONFIDENCE_THRESHOLD:
            request = HITLRequest(
                trigger=HITLTrigger.LOW_OCR_CONFIDENCE,
                reason=f"OCR confidence is {confidence:.1f}% (threshold: {OCR_CONFIDENCE_THRESHOLD}%)",
                current_data={"text": extracted_text, "confidence": confidence},
                agent_source="image_handler",
            )
            self.pending_reviews.append(request)
            return request
        return None

    def check_asr_confidence(self, confidence: float, transcript: str) -> Optional[HITLRequest]:
        """Check if ASR transcript needs human review."""
        if confidence < ASR_CONFIDENCE_THRESHOLD:
            request = HITLRequest(
                trigger=HITLTrigger.LOW_ASR_CONFIDENCE,
                reason=f"ASR confidence is {confidence:.2f} (threshold: {ASR_CONFIDENCE_THRESHOLD})",
                current_data={"text": transcript, "confidence": confidence},
                agent_source="audio_handler",
            )
            self.pending_reviews.append(request)
            return request
        return None

    def check_parser_ambiguity(self, parsed_result: Dict) -> Optional[HITLRequest]:
        """Check if parsed result needs clarification."""
        if parsed_result.get("needs_clarification", False):
            request = HITLRequest(
                trigger=HITLTrigger.PARSER_AMBIGUITY,
                reason=parsed_result.get("clarification_reason", "Parser detected ambiguity in the input"),
                current_data=parsed_result,
                agent_source="parser_agent",
            )
            self.pending_reviews.append(request)
            return request
        return None

    def check_verifier_confidence(self, confidence: float, solution: str, problem: str) -> Optional[HITLRequest]:
        """Check if solution verification needs human review."""
        if confidence < VERIFIER_CONFIDENCE_THRESHOLD:
            request = HITLRequest(
                trigger=HITLTrigger.LOW_VERIFIER_CONFIDENCE,
                reason=f"Verifier confidence is {confidence:.2f} (threshold: {VERIFIER_CONFIDENCE_THRESHOLD})",
                current_data={
                    "solution": solution,
                    "problem": problem,
                    "confidence": confidence,
                },
                agent_source="verifier_agent",
            )
            self.pending_reviews.append(request)
            return request
        return None

    def create_user_review(self, data: Dict, reason: str = "User-initiated review") -> HITLRequest:
        """Create a review request initiated by the user."""
        request = HITLRequest(
            trigger=HITLTrigger.USER_INITIATED,
            reason=reason,
            current_data=data,
            agent_source="user",
        )
        self.pending_reviews.append(request)
        return request

    def resolve_review(self, request: HITLRequest, action: HITLAction,
                       edited_data: Dict = None, comment: str = None) -> Dict:
        """
        Resolve a pending HITL review.

        Returns:
            Dict with 'action' and 'data' — the data to continue with.
        """
        request.resolved = True
        request.action = action
        request.edited_data = edited_data
        request.feedback_comment = comment

        # Move from pending to history
        if request in self.pending_reviews:
            self.pending_reviews.remove(request)
        self.review_history.append(request)

        if action == HITLAction.APPROVE:
            return {"action": "continue", "data": request.current_data}
        elif action == HITLAction.EDIT:
            return {"action": "continue", "data": edited_data or request.current_data}
        elif action == HITLAction.REJECT:
            return {"action": "retry", "data": request.current_data, "comment": comment}

        return {"action": "continue", "data": request.current_data}

    def has_pending_reviews(self) -> bool:
        return len(self.pending_reviews) > 0

    def get_pending_review(self) -> Optional[HITLRequest]:
        """Get the next pending review."""
        return self.pending_reviews[0] if self.pending_reviews else None

    def get_review_summary(self) -> Dict:
        """Get a summary of all reviews."""
        return {
            "pending": len(self.pending_reviews),
            "completed": len(self.review_history),
            "history": [
                {
                    "trigger": r.trigger.value,
                    "action": r.action.value if r.action else None,
                    "reason": r.reason,
                    "agent": r.agent_source,
                }
                for r in self.review_history
            ],
        }
