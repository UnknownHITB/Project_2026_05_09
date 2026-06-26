import os
import sqlite3
import numpy as np
import pytest
from app.core.memory import MemoryManager

@pytest.fixture
def memory_manager(tmp_path):
    db_path = tmp_path / "test_memory.sqlite"
    mm = MemoryManager(db_path=str(db_path))
    # Mock _get_embedding
    mm._get_embedding = lambda x: [0.1, 0.2, 0.3]
    return mm

def test_add_episode_and_semantic_search(memory_manager):
    memory_manager.add_episode("Test summary 1")
    memory_manager._get_embedding = lambda x: [0.5, 0.6, 0.7]
    memory_manager.add_episode("Test summary 2")

    # Search for something close to summary 2
    memory_manager._get_embedding = lambda x: [0.5, 0.6, 0.7]
    results = memory_manager.semantic_search("query")

    assert len(results) > 0
    assert results[0][0] == "Test summary 2"
    assert results[0][2] > 0.99 # Should be almost 1.0

def test_semantic_search_empty(memory_manager):
    results = memory_manager.semantic_search("query")
    assert results == []

def test_semantic_search_no_embedding(memory_manager):
    memory_manager.add_episode("Test summary 1")
    memory_manager._get_embedding = lambda x: None

    # Should fallback to recent episodes
    results = memory_manager.semantic_search("query")
    assert len(results) == 1
    assert results[0][0] == "Test summary 1"
