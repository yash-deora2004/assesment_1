"""Tests for the RAG pipeline."""

import unittest
import os
from rag.indexer import load_documents, chunk_documents, _infer_topic, KNOWLEDGE_BASE_DIR


class TestIndexer(unittest.TestCase):
    """Test cases for the RAG indexer."""

    def test_load_documents(self):
        """Test that knowledge base documents are loaded."""
        docs = load_documents()
        self.assertGreater(len(docs), 0)
        self.assertGreaterEqual(len(docs), 20)  # We have 23 docs

    def test_chunk_documents(self):
        """Test that documents are properly chunked."""
        docs = load_documents()
        chunks = chunk_documents(docs)
        self.assertGreater(len(chunks), len(docs))  # More chunks than docs

        # Each chunk should have text and metadata
        for chunk in chunks:
            self.assertIn("text", chunk)
            self.assertIn("metadata", chunk)
            self.assertIn("source_file", chunk["metadata"])
            self.assertIn("topic", chunk["metadata"])
            self.assertIn("chunk_index", chunk["metadata"])

    def test_infer_topic(self):
        """Test topic inference from filenames."""
        self.assertEqual(_infer_topic("algebra_identities.md"), "algebra")
        self.assertEqual(_infer_topic("prob_basics.md"), "probability")
        self.assertEqual(_infer_topic("calc_limits.md"), "calculus")
        self.assertEqual(_infer_topic("linalg_matrices.md"), "linear_algebra")
        self.assertEqual(_infer_topic("trig_identities.md"), "trigonometry")
        self.assertEqual(_infer_topic("common_mistakes.md"), "general")

    def test_chunk_size(self):
        """Test that chunks respect size limits."""
        docs = load_documents()
        chunks = chunk_documents(docs, chunk_size=500, chunk_overlap=50)
        for chunk in chunks:
            # Chunks can exceed slightly due to splitting logic, but shouldn't be massive
            self.assertLess(len(chunk["text"]), 1000)


class TestKnowledgeBase(unittest.TestCase):
    """Test that all expected knowledge base files exist."""

    EXPECTED_FILES = [
        "algebra_identities.md", "algebra_equations.md", "algebra_inequalities.md",
        "algebra_sequences.md", "algebra_logarithms.md", "algebra_complex_numbers.md",
        "prob_basics.md", "prob_conditional.md", "prob_distributions.md",
        "prob_permutations.md", "calc_limits.md", "calc_derivatives.md",
        "calc_applications.md", "calc_integration_basics.md", "linalg_matrices.md",
        "linalg_determinants.md", "linalg_vectors.md", "linalg_systems.md",
        "common_mistakes.md", "solution_templates.md", "domain_constraints.md",
        "trig_identities.md", "jee_tips.md",
    ]

    def test_all_files_exist(self):
        """Test that all 23 knowledge base files exist."""
        for filename in self.EXPECTED_FILES:
            path = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            self.assertTrue(os.path.exists(path), f"Missing: {filename}")

    def test_files_not_empty(self):
        """Test that knowledge base files are not empty."""
        for filename in self.EXPECTED_FILES:
            path = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            size = os.path.getsize(path)
            self.assertGreater(size, 100, f"File too small: {filename}")


if __name__ == "__main__":
    unittest.main()
