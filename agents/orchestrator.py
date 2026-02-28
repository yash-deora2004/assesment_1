"""
Agent Orchestrator — Coordinates the full pipeline: Parser → Router → Solver → Verifier → Explainer.
"""

import time
from typing import Dict, Any, List, Optional

from openai import OpenAI

from agents.parser_agent import ParserAgent
from agents.router_agent import RouterAgent
from agents.solver_agent import SolverAgent
from agents.verifier_agent import VerifierAgent
from agents.explainer_agent import ExplainerAgent
from rag.retriever import Retriever
from memory.store import MemoryStore
from hitl.review import HITLManager, HITLTrigger

MAX_SOLVER_RETRIES = 2


class AgentOrchestrator:
    """Orchestrates the multi-agent pipeline for solving math problems."""

    def __init__(self, client: OpenAI = None, index_path: str = None):
        self.client = client or OpenAI()

        # Initialize agents
        self.parser = ParserAgent(self.client)
        self.router = RouterAgent(self.client)
        self.solver = SolverAgent(self.client)
        self.verifier = VerifierAgent(self.client)
        self.explainer = ExplainerAgent(self.client)

        # Initialize supporting systems
        retriever_kwargs = {"client": self.client}
        if index_path:
            retriever_kwargs["index_path"] = index_path
        self.retriever = Retriever(**retriever_kwargs)

        self.memory = MemoryStore(client=self.client)
        self.hitl_manager = HITLManager()

        # Trace log
        self.trace_log: List[Dict] = []

    def run(self, raw_text: str, input_type: str = "text") -> Dict[str, Any]:
        """
        Run the full agent pipeline.

        Args:
            raw_text: The input text (from OCR, ASR, or direct text).
            input_type: One of 'text', 'image', 'audio'.

        Returns:
            Complete result dict with all pipeline outputs.
        """
        self.trace_log = []
        result = {
            "input": raw_text,
            "input_type": input_type,
            "status": "in_progress",
        }

        # --- Step 1: Parse ---
        parse_start = time.time()
        correction_rules = self.memory.get_correction_rules()
        parse_result = self.parser.parse(raw_text, input_type, correction_rules)
        parse_time = time.time() - parse_start

        parsed = parse_result["parsed"]
        trace_entry = parse_result["trace"]
        trace_entry["duration_s"] = round(parse_time, 2)
        self.trace_log.append(trace_entry)

        result["parsed_problem"] = parsed

        # Check for HITL trigger: parser ambiguity
        hitl_request = self.hitl_manager.check_parser_ambiguity(parsed)
        if hitl_request:
            result["hitl_needed"] = True
            result["hitl_request"] = {
                "trigger": hitl_request.trigger.value,
                "reason": hitl_request.reason,
                "data": hitl_request.current_data,
            }
            result["status"] = "awaiting_hitl"
            result["trace"] = self.trace_log
            return result

        # --- Step 2: Route ---
        route_start = time.time()
        route_result = self.router.route(parsed)
        route_time = time.time() - route_start

        routing = route_result["routing"]
        trace_entry = route_result["trace"]
        trace_entry["duration_s"] = round(route_time, 2)
        self.trace_log.append(trace_entry)

        result["routing"] = routing

        # --- Step 3: Retrieve RAG context ---
        rag_start = time.time()
        try:
            rag_result = self.retriever.retrieve_with_sources(
                parsed.get("problem_text", raw_text),
                top_k=5,
                topic_filter=routing.get("topic"),
            )
        except Exception:
            # If RAG fails (e.g., index not built), continue without context
            rag_result = {
                "chunks": [],
                "has_relevant_context": False,
                "message": "RAG index not available.",
            }
        rag_time = time.time() - rag_start

        rag_context = self.retriever.format_context(rag_result.get("chunks", []))
        rag_sources = rag_result.get("sources", [])

        self.trace_log.append({
            "agent": "RAG Retriever",
            "input": parsed.get("problem_text", raw_text)[:100],
            "output": {
                "has_context": rag_result.get("has_relevant_context", False),
                "num_chunks": len(rag_result.get("chunks", [])),
                "sources": rag_sources,
            },
            "duration_s": round(rag_time, 2),
        })

        result["rag"] = {
            "has_context": rag_result.get("has_relevant_context", False),
            "chunks": rag_result.get("chunks", []),
            "sources": rag_sources,
        }

        # --- Step 3b: Check memory for similar problems ---
        similar_problems = []
        try:
            similar_problems = self.memory.find_similar(
                parsed.get("problem_text", raw_text), top_k=3
            )
        except Exception:
            pass

        result["similar_problems"] = similar_problems

        # --- Step 4: Solve (with retry loop) ---
        verifier_feedback = None
        solution = None
        verification = None

        for attempt in range(1, MAX_SOLVER_RETRIES + 2):
            # Solve
            solve_start = time.time()
            solve_result = self.solver.solve(
                parsed, routing, rag_context, rag_sources,
                similar_problems, verifier_feedback,
            )
            solve_time = time.time() - solve_start

            solution = solve_result["solution"]
            trace_entry = solve_result["trace"]
            trace_entry["duration_s"] = round(solve_time, 2)
            trace_entry["attempt"] = attempt
            self.trace_log.append(trace_entry)

            # Verify
            verify_start = time.time()
            verify_result = self.verifier.verify(parsed, solution)
            verify_time = time.time() - verify_start

            verification = verify_result["verification"]
            trace_entry = verify_result["trace"]
            trace_entry["duration_s"] = round(verify_time, 2)
            trace_entry["attempt"] = attempt
            self.trace_log.append(trace_entry)

            # Check verification result
            if verification.get("is_correct", False) and verification.get("confidence", 0) >= 0.7:
                break

            if attempt <= MAX_SOLVER_RETRIES:
                verifier_feedback = verification.get("suggested_fix") or verification.get("feedback", "")
            else:
                # Max retries reached — check HITL
                hitl_request = self.hitl_manager.check_verifier_confidence(
                    verification.get("confidence", 0),
                    solution.get("final_answer", ""),
                    parsed.get("problem_text", ""),
                )
                if hitl_request:
                    result["hitl_needed"] = True
                    result["hitl_request"] = {
                        "trigger": hitl_request.trigger.value,
                        "reason": hitl_request.reason,
                        "data": hitl_request.current_data,
                    }

        result["solution"] = solution
        result["verification"] = verification

        # --- Step 5: Explain ---
        explain_start = time.time()
        explain_result = self.explainer.explain(
            parsed, solution, verification, rag_sources,
        )
        explain_time = time.time() - explain_start

        explanation = explain_result["explanation"]
        trace_entry = explain_result["trace"]
        trace_entry["duration_s"] = round(explain_time, 2)
        self.trace_log.append(trace_entry)

        result["explanation"] = explanation
        result["confidence"] = verification.get("confidence", 0)
        result["status"] = "completed"
        result["trace"] = self.trace_log

        # Store in memory
        try:
            memory_id = self.memory.store({
                "input_type": input_type,
                "original_input_ref": raw_text,
                "parsed_problem": parsed,
                "topic": routing.get("topic", parsed.get("topic")),
                "retrieved_context": rag_sources,
                "solution": explanation.get("explanation", ""),
                "steps": [s.get("work", str(s)) for s in solution.get("steps", [])],
                "verifier_confidence": verification.get("confidence", 0),
                "verifier_outcome": "pass" if verification.get("is_correct") else "fail",
            })
            result["memory_id"] = memory_id
        except Exception:
            pass

        return result

    def process_hitl_response(self, result: Dict, action: str,
                              edited_text: str = None, comment: str = None) -> Dict:
        """
        Continue the pipeline after HITL response.

        Args:
            result: The previous result that triggered HITL.
            action: One of 'approve', 'edit', 'reject'.
            edited_text: The edited text (if action is 'edit').
            comment: User comment.

        Returns:
            Updated result after continuing the pipeline.
        """
        if action == "edit" and edited_text:
            # Re-run with edited input
            return self.run(edited_text, result.get("input_type", "text"))
        elif action == "reject":
            # Re-run with feedback
            return self.run(result.get("input", ""), result.get("input_type", "text"))
        else:
            # Approve — mark as complete
            result["status"] = "completed"
            result["hitl_needed"] = False
            return result
