import time
import sqlite3
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.memory import MemoryManager

def benchmark_optimizations():
    db_path = "bench_final.sqlite"
    if os.path.exists(db_path):
        os.remove(db_path)

    memory = MemoryManager(db_path=db_path)

    # 1. Benchmark Sequential vs Consolidated
    print("Benchmarking database retrieval overhead...")

    iterations = 100

    # Pre-fill data
    memory.store_fact("user", "name", "Bolt")
    memory.add_episode("Test episode")
    memory.set_rule("test", "test rule")

    # Sequential calls (Original logic)
    start = time.time()
    for _ in range(iterations):
        memory.get_facts(entity='user')
        memory.get_recent_episodes(limit=3)
        memory.get_all_rules()
    t_seq = (time.time() - start) / iterations
    print(f"Average time (3 sequential calls): {t_seq*1000:.3f}ms")

    # Consolidated call (Optimized logic)
    start = time.time()
    for _ in range(iterations):
        memory.get_full_context(entity='user', episodes_limit=3)
    t_opt = (time.time() - start) / iterations
    print(f"Average time (1 consolidated call): {t_opt*1000:.3f}ms")

    print(f"Database overhead reduction: {(1 - t_opt/t_seq)*100:2.1f}%")

    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    benchmark_optimizations()
