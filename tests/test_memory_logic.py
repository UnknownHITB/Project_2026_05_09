import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock heavy/hardware dependencies
mock_modules = [
    "pyaudio",
    "sounddevice",
    "cv2",
    "pyautogui",
    "faster_whisper",
    "kokoro",
    "AppOpener",
    "ddgs"
]

for mod_name in mock_modules:
    sys.modules[mod_name] = MagicMock()

import numpy as np
from app.core.memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_memory_logic.sqlite"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.mm = MemoryManager(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        # Also cleanup WAL files
        for ext in ["-shm", "-wal"]:
            if os.path.exists(self.db_path + ext):
                os.remove(self.db_path + ext)

    def test_store_and_get_fact(self):
        self.mm.store_fact("user", "name", "Alice")
        facts = self.mm.get_facts("user")
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0], ("name", "Alice"))

    @patch("app.core.memory.MemoryManager._get_embedding")
    def test_semantic_search_vectorized(self, mock_embedding):
        # Mock embeddings (dim=3)
        dim = 3
        # episode 1: [1, 0, 0]
        # episode 2: [0, 1, 0]
        # query: [1, 0.1, 0] -> should be closer to episode 1

        mock_embedding.side_effect = [
            [1.0, 0.0, 0.0], # for episode 1
            [0.0, 1.0, 0.0], # for episode 2
            [1.0, 0.1, 0.0]  # for query
        ]

        self.mm.add_episode("episode 1")
        self.mm.add_episode("episode 2")

        results = self.mm.semantic_search("query", limit=2)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], "episode 1")
        self.assertEqual(results[1][0], "episode 2")
        self.assertTrue(results[0][2] > results[1][2])

    @patch("app.core.memory.MemoryManager._get_embedding")
    def test_semantic_search_empty(self, mock_embedding):
        mock_embedding.return_value = [1.0, 0.0, 0.0]
        results = self.mm.semantic_search("query")
        self.assertEqual(results, [])

    @patch("app.core.memory.MemoryManager._get_embedding")
    def test_semantic_search_zero_norm(self, mock_embedding):
        mock_embedding.return_value = [0.0, 0.0, 0.0]
        self.mm.add_episode("something")
        results = self.mm.semantic_search("query")
        # Should return recent episodes with 0.0 similarity
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][2], 0.0)

if __name__ == "__main__":
    unittest.main()
