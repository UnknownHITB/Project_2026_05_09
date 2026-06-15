import pytest
import os
import numpy as np
import sqlite3
import time
from app.core.memory import MemoryManager

@pytest.fixture
def memory_manager():
    db_path = "test_memory_opt.sqlite"
    if os.path.exists(db_path):
        os.remove(db_path)
    mm = MemoryManager(db_path=db_path)
    yield mm
    if os.path.exists(db_path):
        os.remove(db_path)

def test_get_full_context(memory_manager):
    # Setup
    memory_manager.store_fact("user", "name", "Alice")
    memory_manager.store_fact("other", "key", "val")
    memory_manager.set_rule("r1", "Be polite")

    # Mock embedding to avoid network calls
    memory_manager._get_embedding = lambda x: [0.1, 0.2, 0.3]

    # Use manual insertion with explicit timestamps to guarantee order in tests
    with sqlite3.connect(memory_manager.db_path) as conn:
        conn.execute("INSERT INTO episodic_memory (summary, timestamp) VALUES (?, ?)", ("Entry 1", "2023-01-01 00:00:00"))
        conn.execute("INSERT INTO episodic_memory (summary, timestamp) VALUES (?, ?)", ("Entry 2", "2023-01-01 00:00:01"))

    # Execute
    facts, episodes, rules = memory_manager.get_full_context()

    # Verify
    assert len(facts) == 1
    assert facts[0] == ("name", "Alice")
    assert len(rules) == 1
    assert "Be polite" in rules
    assert len(episodes) == 2
    # episodes are ordered by timestamp DESC
    assert episodes[0][0] == "Entry 2"
    assert episodes[1][0] == "Entry 1"

def test_semantic_search_vectorization(memory_manager):
    # Setup vectors
    v1 = [1.0, 0.0, 0.0]
    v2 = [0.0, 1.0, 0.0]
    v3 = [0.7, 0.7, 0.0] # Should be close to both

    # Manually insert to avoid network calls
    with sqlite3.connect(memory_manager.db_path) as conn:
        conn.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("V1", np.array(v1, dtype=np.float32).tobytes()))
        conn.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("V2", np.array(v2, dtype=np.float32).tobytes()))
        conn.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("V3", np.array(v3, dtype=np.float32).tobytes()))

    # Mock query embedding
    memory_manager._get_embedding = lambda x: v1

    # Execute
    results = memory_manager.semantic_search("query", limit=3)

    # Verify
    assert results[0][0] == "V1"
    assert results[1][0] == "V3"
    assert results[2][0] == "V2"
    # Check similarity values are floats and in expected range
    assert isinstance(results[0][2], float)
    assert results[0][2] > 0.99
    assert results[1][2] > 0.5
    assert results[2][2] < 0.1

def test_semantic_search_empty(memory_manager):
    results = memory_manager.semantic_search("anything")
    assert results == []

def test_semantic_search_zero_norm(memory_manager):
    # Vector of all zeros
    v_zero = [0.0, 0.0, 0.0]
    with sqlite3.connect(memory_manager.db_path) as conn:
        conn.execute("INSERT INTO episodic_memory (summary, vector) VALUES (?, ?)", ("ZERO", np.array(v_zero, dtype=np.float32).tobytes()))

    memory_manager._get_embedding = lambda x: [1.0, 0.0, 0.0]
    results = memory_manager.semantic_search("query")

    # Should not crash and should return zero similarity
    if results:
        assert results[0][2] == 0.0
