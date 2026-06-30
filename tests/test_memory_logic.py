import unittest
import numpy as np
import os
import sqlite3
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.core.memory import MemoryManager

class TestMemoryLogic(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_memory.sqlite"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.mm = MemoryManager(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        # Clean up SQLite sidecar files
        for suffix in ["-shm", "-wal"]:
            sidecar = self.db_path + suffix
            if os.path.exists(sidecar):
                os.remove(sidecar)

    def test_semantic_search_empty(self):
        # Should return empty list if no episodes
        results = self.mm.semantic_search("test")
        self.assertEqual(results, [])

    def test_semantic_search_correctness(self):
        # Mock _get_embedding to return specific vectors
        # Vector dim = 3 for simplicity
        vec1 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        vec2 = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        vec3 = np.array([0.5, 0.5, 0.0], dtype=np.float32)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("Topic A", vec1.tobytes()))
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("Topic B", vec2.tobytes()))
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("Topic C", vec3.tobytes()))
            conn.commit()

        # Search for something close to Topic A
        self.mm._get_embedding = lambda x: [0.9, 0.1, 0.0]
        results = self.mm.semantic_search("query close to A", limit=1)
        self.assertEqual(results[0][0], "Topic A")
        self.assertGreater(results[0][2], 0.9)

        # Search for something close to Topic B
        self.mm._get_embedding = lambda x: [0.1, 0.9, 0.0]
        results = self.mm.semantic_search("query close to B", limit=1)
        self.assertEqual(results[0][0], "Topic B")
        self.assertGreater(results[0][2], 0.9)

    def test_semantic_search_zero_norm(self):
        # Test handling of zero-norm vectors (should not crash)
        vec_zero = np.zeros(3, dtype=np.float32)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("Zero", vec_zero.tobytes()))
            conn.commit()

        self.mm._get_embedding = lambda x: [1.0, 0.0, 0.0]
        results = self.mm.semantic_search("test")
        self.assertEqual(results[0][0], "Zero")
        self.assertEqual(results[0][2], 0.0)

if __name__ == "__main__":
    unittest.main()
