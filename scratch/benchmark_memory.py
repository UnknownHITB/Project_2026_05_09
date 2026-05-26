import time
import sys
import os
import sqlite3

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.curdir))

from app.core.memory import memory

def benchmark():
    # Warm up and ensure some data exists
    memory.store_fact("user", "name", "Bolt")
    memory.add_episode("Initial benchmark episode")
    memory.set_rule("Be fast", "Always optimize for speed.")

    print("Starting benchmark (100 iterations)...")

    # Current/Old approach (simulated by calling individual methods)
    start_old = time.perf_counter()
    for _ in range(100):
        facts = memory.get_facts(entity='user')
        episodes = memory.get_recent_episodes(limit=3)
        rules = memory.get_all_rules()
    end_old = time.perf_counter()
    avg_old = (end_old - start_old) / 100 * 1000

    # New Optimized approach
    start_new = time.perf_counter()
    for _ in range(100):
        context = memory.get_full_context(entity='user', episodic_limit=3)
    end_new = time.perf_counter()
    avg_new = (end_new - start_new) / 100 * 1000

    print(f"Average retrieval time (Individual calls): {avg_old:.4f} ms")
    print(f"Average retrieval time (Consolidated):     {avg_new:.4f} ms")

    if avg_new < avg_old:
        improvement = (avg_old - avg_new) / avg_old * 100
        print(f"⚡ Performance Boost: {improvement:.2f}% faster")
    else:
        print("No measurable improvement in this environment.")

if __name__ == "__main__":
    benchmark()
