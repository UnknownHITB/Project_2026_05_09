import unittest
import os
import sqlite3
import time
from app.core.memory import MemoryManager

class TestMemoryManagerConsolidation(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_memory_unit.sqlite"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.memory = MemoryManager(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_full_context(self):
        # Seed data
        self.memory.store_fact("user", "name", "Bolt")
        self.memory.store_fact("user", "hobby", "Performance")

        # Manually insert to guarantee order if timestamps are too close
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO episodic_memory (summary, timestamp) VALUES (?, ?)", ("First episode", "2025-01-01 10:00:00"))
            conn.execute("INSERT INTO episodic_memory (summary, timestamp) VALUES (?, ?)", ("Second episode", "2025-01-01 10:01:00"))
            conn.commit()

        self.memory.set_rule("Speed", "Always be fast.")

        # Test consolidated call
        facts, episodes, rules = self.memory.get_full_context()

        # Verify facts
        self.assertEqual(len(facts), 2)
        fact_dict = dict(facts)
        self.assertEqual(fact_dict["name"], "Bolt")
        self.assertEqual(fact_dict["hobby"], "Performance")

        # Verify episodes (ordered by timestamp DESC, limit 3)
        self.assertEqual(len(episodes), 2)
        # The most recent one should be first
        self.assertEqual(episodes[0][0], "Second episode")
        self.assertEqual(episodes[1][0], "First episode")

        # Verify rules
        self.assertIn("Always be fast.", rules)

if __name__ == "__main__":
    unittest.main()
