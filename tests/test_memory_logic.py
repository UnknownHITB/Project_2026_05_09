import os
import sqlite3
import numpy as np
import unittest
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_memory.sqlite"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.mm = MemoryManager(db_path=self.db_path)

    def tearDown(self):
        # Close connections if any are open
        import gc
        gc.collect()

        for suffix in ["", "-shm", "-wal"]:
            path = self.db_path + suffix
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass

    def test_semantic_search_functionality(self):
        # Mock embeddings for predictable results
        # 3 dimensions for simplicity
        embeddings = {
            "apple": [1.0, 0.0, 0.0],
            "banana": [0.0, 1.0, 0.0],
            "cherry": [0.0, 0.0, 1.0],
            "red fruit": [0.9, 0.0, 0.1]
        }

        def mock_get_embedding(text):
            return embeddings.get(text, [0.5, 0.5, 0.5])

        self.mm._get_embedding = mock_get_embedding

        # Add episodes
        self.mm.add_episode("apple", "fruit")
        self.mm.add_episode("banana", "fruit")
        self.mm.add_episode("cherry", "fruit")

        # Search for "red fruit"
        results = self.mm.semantic_search("red fruit", limit=2)

        self.assertEqual(len(results), 2)
        # "apple" should be the most similar to "red fruit" (0.9 vs others)
        self.assertEqual(results[0][0], "apple")
        self.assertGreater(results[0][2], results[1][2])

    def test_semantic_search_empty(self):
        results = self.mm.semantic_search("nothing")
        self.assertEqual(results, [])

    def test_semantic_search_no_embedding(self):
        self.mm._get_embedding = lambda x: None
        self.mm.add_episode("test", "test")

        # Should fallback to recent episodes with 0.0 similarity
        results = self.mm.semantic_search("query")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "test")
        self.assertEqual(results[0][2], 0.0)

    def test_zero_norm_vector(self):
        # Case where a stored vector is all zeros
        self.mm._get_embedding = lambda x: [1.0, 0.0, 0.0]

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            zero_vec = np.zeros(3, dtype=np.float32).tobytes()
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("zero", zero_vec))
            conn.commit()

        results = self.mm.semantic_search("query")
        # Should not crash and should have 0.0 similarity for the zero vector
        self.assertEqual(results[0][0], "zero")
        self.assertEqual(results[0][2], 0.0)

if __name__ == "__main__":
    unittest.main()
