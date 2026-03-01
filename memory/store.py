"""
Memory Store — SQLite + FAISS memory backend for self-learning.
"""

import os
import json
import uuid
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any

import numpy as np
from openai import OpenAI
import faiss

from rag.indexer import embed_texts, EMBEDDING_DIM

DEFAULT_DB_PATH = os.getenv("MEMORY_DB_PATH", os.path.join("data", "memory.db"))
MEMORY_INDEX_PATH = os.path.join("data", "memory_index")
CORRECTION_RULES_PATH = os.path.join(os.path.dirname(__file__), "correction_rules.json")
SIMILARITY_THRESHOLD = 0.75


class MemoryStore:
    """Stores past interactions and enables similar-problem retrieval."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH, client: OpenAI = None):
        self.db_path = db_path
        self.client = client or OpenAI()
        self._faiss_index = None
        self._memory_ids = []  # Maps FAISS index position → memory ID
        self._init_db()
        self._load_faiss_index()

    def _init_db(self):
        """Initialize the SQLite database schema."""
        os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else ".", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                input_type TEXT,
                original_input_ref TEXT,
                ocr_asr_output TEXT,
                parsed_problem TEXT,
                topic TEXT,
                retrieved_context TEXT,
                solution TEXT,
                steps TEXT,
                verifier_confidence REAL,
                verifier_outcome TEXT,
                user_feedback TEXT,
                user_comment TEXT,
                correction_applied TEXT,
                embedding BLOB
            )
        """)
        conn.commit()
        conn.close()

    def _load_faiss_index(self):
        """Load or create the FAISS memory index."""
        index_file = os.path.join(MEMORY_INDEX_PATH, "memory.faiss")
        ids_file = os.path.join(MEMORY_INDEX_PATH, "memory_ids.json")

        if os.path.exists(index_file) and os.path.exists(ids_file):
            self._faiss_index = faiss.read_index(index_file)
            with open(ids_file, "r", encoding="utf-8") as f:
                self._memory_ids = json.load(f)
        else:
            self._faiss_index = faiss.IndexFlatIP(EMBEDDING_DIM)
            self._memory_ids = []

    def _save_faiss_index(self):
        """Persist the FAISS memory index to disk."""
        os.makedirs(MEMORY_INDEX_PATH, exist_ok=True)
        faiss.write_index(
            self._faiss_index,
            os.path.join(MEMORY_INDEX_PATH, "memory.faiss"),
        )
        with open(os.path.join(MEMORY_INDEX_PATH, "memory_ids.json"), "w", encoding="utf-8") as f:
            json.dump(self._memory_ids, f)

    def store(self, interaction: Dict[str, Any]) -> str:
        """
        Store a new interaction in memory.

        Args:
            interaction: Dict with keys matching the memory schema.

        Returns:
            The generated memory ID.
        """
        memory_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Generate embedding for the parsed problem
        problem_text = ""
        if isinstance(interaction.get("parsed_problem"), dict):
            problem_text = interaction["parsed_problem"].get("problem_text", "")
        elif isinstance(interaction.get("parsed_problem"), str):
            problem_text = interaction["parsed_problem"]

        embedding = None
        embedding_blob = None
        if problem_text:
            embedding = embed_texts([problem_text], self.client)
            faiss.normalize_L2(embedding)
            embedding_blob = embedding.tobytes()

            # Add to FAISS index
            self._faiss_index.add(embedding)
            self._memory_ids.append(memory_id)
            self._save_faiss_index()

        # Store in SQLite
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            INSERT INTO memories
            (id, timestamp, input_type, original_input_ref, ocr_asr_output,
             parsed_problem, topic, retrieved_context, solution, steps,
             verifier_confidence, verifier_outcome, user_feedback,
             user_comment, correction_applied, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                memory_id,
                timestamp,
                interaction.get("input_type"),
                interaction.get("original_input_ref"),
                interaction.get("ocr_asr_output"),
                json.dumps(interaction.get("parsed_problem")) if isinstance(interaction.get("parsed_problem"), dict) else interaction.get("parsed_problem"),
                interaction.get("topic"),
                json.dumps(interaction.get("retrieved_context")) if isinstance(interaction.get("retrieved_context"), list) else interaction.get("retrieved_context"),
                interaction.get("solution"),
                json.dumps(interaction.get("steps")) if isinstance(interaction.get("steps"), list) else interaction.get("steps"),
                interaction.get("verifier_confidence"),
                interaction.get("verifier_outcome"),
                interaction.get("user_feedback"),
                interaction.get("user_comment"),
                interaction.get("correction_applied"),
                embedding_blob,
            ),
        )
        conn.commit()
        conn.close()

        return memory_id

    def find_similar(self, problem_text: str, top_k: int = 3) -> List[Dict]:
        """
        Find similar past problems using FAISS similarity search.

        Returns:
            List of similar memory records with similarity scores.
        """
        if self._faiss_index.ntotal == 0:
            return []

        query_embedding = embed_texts([problem_text], self.client)
        faiss.normalize_L2(query_embedding)

        k = min(top_k, self._faiss_index.ntotal)
        scores, indices = self._faiss_index.search(query_embedding, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or score < SIMILARITY_THRESHOLD:
                continue

            memory_id = self._memory_ids[idx]
            record = self._get_record(memory_id)
            if record:
                record["similarity_score"] = float(score)
                results.append(record)

        return results

    def _get_record(self, memory_id: str) -> Optional[Dict]:
        """Retrieve a single memory record by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM memories WHERE id = ?", (memory_id,)).fetchone()
        conn.close()

        if not row:
            return None

        record = dict(row)
        # Remove binary embedding from result
        record.pop("embedding", None)

        # Parse JSON fields
        for field in ["parsed_problem", "retrieved_context", "steps"]:
            if record.get(field):
                try:
                    record[field] = json.loads(record[field])
                except (json.JSONDecodeError, TypeError):
                    pass

        return record

    def update_feedback(self, memory_id: str, feedback: str, comment: str = None):
        """Update user feedback for a stored interaction."""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "UPDATE memories SET user_feedback = ?, user_comment = ? WHERE id = ?",
            (feedback, comment, memory_id),
        )
        conn.commit()
        conn.close()

    def get_correction_rules(self) -> Dict:
        """Load OCR/ASR correction rules from JSON."""
        if os.path.exists(CORRECTION_RULES_PATH):
            with open(CORRECTION_RULES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"ocr_corrections": {}, "asr_corrections": {}, "learned_corrections": []}

    def add_correction_rule(self, wrong: str, correct: str, source: str = "user"):
        """Add a learned correction rule."""
        rules = self.get_correction_rules()
        rules["learned_corrections"].append({
            "wrong": wrong,
            "correct": correct,
            "source": source,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        })
        with open(CORRECTION_RULES_PATH, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)

    def apply_corrections(self, text: str, input_type: str = "text") -> str:
        """Apply known correction rules to input text."""
        rules = self.get_correction_rules()

        if input_type == "image":
            for wrong, correct in rules.get("ocr_corrections", {}).items():
                text = text.replace(wrong, correct)
        elif input_type == "audio":
            for wrong, correct in rules.get("asr_corrections", {}).items():
                text = text.replace(wrong, correct)

        # Apply learned corrections
        for rule in rules.get("learned_corrections", []):
            text = text.replace(rule["wrong"], rule["correct"])

        return text

    def get_all_memories(self, limit: int = 50) -> List[Dict]:
        """Get recent memories for display."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM memories ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()

        results = []
        for row in rows:
            record = dict(row)
            record.pop("embedding", None)
            for field in ["parsed_problem", "retrieved_context", "steps"]:
                if record.get(field):
                    try:
                        record[field] = json.loads(record[field])
                    except (json.JSONDecodeError, TypeError):
                        pass
            results.append(record)

        return results
