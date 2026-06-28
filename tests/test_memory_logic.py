import numpy as np
import sqlite3
import os
import sys
from pathlib import Path
import unittest
from unittest.mock import MagicMock

# Add project root to sys.path
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.core.memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_pytest_memory.sqlite"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.memory = MemoryManager(db_path=self.db_path)
        # Mock _get_embedding to avoid network calls
        self.memory._get_embedding = MagicMock()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        for suffix in ["-shm", "-wal"]:
            if os.path.exists(self.db_path + suffix):
                os.remove(self.db_path + suffix)

    def test_semantic_search_vectorization(self):
        v1 = np.array([1, 0, 0], dtype=np.float32)
        v2 = np.array([0, 1, 0], dtype=np.float32)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("V1", v1.tobytes()))
            cursor.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("V2", v2.tobytes()))
            conn.commit()

        self.memory._get_embedding.return_value = [1, 0.1, 0]
        results = self.memory.semantic_search("test")

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], "V1")
        self.assertGreater(results[0][2], results[1][2])

    def test_wal_mode_enabled(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode")
            mode = cursor.fetchone()[0]
            self.assertEqual(mode.lower(), "wal")

if __name__ == "__main__":
    unittest.main()
