import pytest
import os
import sqlite3
import numpy as np
from app.core.memory import MemoryManager

@pytest.fixture
def memory_manager():
    db_path = "test_memory.sqlite"
    if os.path.exists(db_path):
        os.remove(db_path)
    mm = MemoryManager(db_path)
    yield mm
    if os.path.exists(db_path):
        os.remove(db_path)

def test_get_full_context(memory_manager):
    # Setup data
    memory_manager.store_fact("user", "hobby", "coding")
    memory_manager.add_episode("User started a new project")
    memory_manager.set_rule("logic", "Use clean code")

    # Test retrieval
    context = memory_manager.get_full_context(entity='user')

    assert "facts" in context
    assert "episodes" in context
    assert "rules" in context

    assert any(attr == "hobby" and val == "coding" for attr, val in context["facts"])
    assert any("User started a new project" in s for s, _ in context["episodes"])
    assert "Use clean code" in context["rules"]

def test_wal_mode(memory_manager):
    with sqlite3.connect(memory_manager.db_path) as conn:
        cursor = conn.execute("PRAGMA journal_mode")
        mode = cursor.fetchone()[0]
        assert mode.lower() == "wal"
