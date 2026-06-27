import unittest
import numpy as np
import os
import sqlite3
from app.core.memory import MemoryManager

class TestMemoryLogic(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_memory.sqlite"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.memory = MemoryManager(db_path=self.db_path)
        self.dim = 768

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_semantic_search_basic(self):
        # Insert a few known vectors
        v1 = np.zeros(self.dim, dtype=np.float32)
        v1[0] = 1.0
        v2 = np.zeros(self.dim, dtype=np.float32)
        v2[1] = 1.0

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("Topic A", v1.tobytes()))
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("Topic B", v2.tobytes()))
            conn.commit()

        # Mock _get_embedding to return v1
        self.memory._get_embedding = lambda x: v1.tolist()

        results = self.memory.semantic_search("dummy", limit=2)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], "Topic A")
        self.assertAlmostEqual(results[0][2], 1.0)
        self.assertAlmostEqual(results[1][2], 0.0)

    def test_semantic_search_limit(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for i in range(10):
                vec = np.random.rand(self.dim).astype(np.float32)
                cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", (f"Summary {i}", vec.tobytes()))
            conn.commit()

        self.memory._get_embedding = lambda x: np.random.rand(self.dim).tolist()
        results = self.memory.semantic_search("dummy", limit=3)
        self.assertEqual(len(results), 3)

    def test_zero_norm_handling(self):
        # Insert a zero vector
        v_zero = np.zeros(self.dim, dtype=np.float32)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("Zero", v_zero.tobytes()))
            conn.commit()

        self.memory._get_embedding = lambda x: np.random.rand(self.dim).tolist()
        results = self.memory.semantic_search("dummy")
        # Should not crash and similarity should be 0.0
        self.assertEqual(results[0][0], "Zero")
        self.assertEqual(results[0][2], 0.0)

if __name__ == "__main__":
    unittest.main()
