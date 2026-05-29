import time
import sqlite3
import os
import sys

# Add current directory to sys.path
sys.path.insert(0, os.getcwd())

from app.core.memory import MemoryManager

def benchmark_separate_calls(memory, iterations=100):
    start_time = time.time()
    for _ in range(iterations):
        facts = memory.get_facts(entity='user')
        episodes = memory.get_recent_episodes(limit=3)
        rules = memory.get_all_rules()
    end_time = time.time()
    return (end_time - start_time) / iterations

def get_full_context_mock(self):
    with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT attribute, value FROM semantic_memory WHERE entity = ?", ('user',))
        facts = cursor.fetchall()

        cursor.execute("SELECT summary, timestamp FROM episodic_memory ORDER BY timestamp DESC LIMIT 3")
        episodes = cursor.fetchall()

        cursor.execute("SELECT rule_content FROM procedural_memory")
        rules = [row[0] for row in cursor.fetchall()]

        return facts, episodes, rules

def benchmark_consolidated_call(memory, iterations=100):
    # Temporarily add the method if it doesn't exist
    if not hasattr(MemoryManager, 'get_full_context'):
        MemoryManager.get_full_context = get_full_context_mock

    start_time = time.time()
    for _ in range(iterations):
        facts, episodes, rules = memory.get_full_context()
    end_time = time.time()
    return (end_time - start_time) / iterations

def main():
    db_path = "test_memory.sqlite"
    if os.path.exists(db_path):
        os.remove(db_path)

    memory = MemoryManager(db_path=db_path)

    # Add some data
    memory.store_fact("user", "name", "Bolt")
    memory.store_fact("user", "hobby", "Speed")
    for i in range(10):
        memory.add_episode(f"Episode {i}", "test")
    for i in range(5):
        memory.set_rule(f"Rule {i}", f"Content {i}")

    print("Benchmarking separate calls...")
    avg_separate = benchmark_separate_calls(memory)
    print(f"Average time (separate): {avg_separate*1000:.4f} ms")

    print("Benchmarking consolidated call...")
    avg_consolidated = benchmark_consolidated_call(memory)
    print(f"Average time (consolidated): {avg_consolidated*1000:.4f} ms")

    improvement_ms = (avg_separate - avg_consolidated) * 1000
    improvement_pct = (avg_separate - avg_consolidated) / avg_separate * 100
    print(f"Improvement: {improvement_ms:.4f} ms ({improvement_pct:.2f}%)")

    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    main()
