import sqlite3
import json
import os
import numpy as np
import requests
from datetime import datetime

class MemoryManager:
    def __init__(self, db_path="memory.sqlite"):
        self.db_path = db_path
        self._init_db()
        self.session = requests.Session()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            # Semantic Memory: Facts & Knowledge
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS semantic_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity TEXT,
                    attribute TEXT,
                    value TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(entity, attribute)
                )
            """)
            # Episodic Memory: Past Experiences / Summaries + Embeddings
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS episodic_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    summary TEXT,
                    keywords TEXT,
                    vector BLOB,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Procedural Memory: System Behavior / Rules
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS procedural_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_name TEXT UNIQUE,
                    rule_content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Simple migration: Add vector column if it doesn't exist
            cursor.execute("PRAGMA table_info(episodic_memory)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'vector' not in columns:
                cursor.execute("ALTER TABLE episodic_memory ADD COLUMN vector BLOB")
                
            conn.commit()

    # --- Semantic Memory Methods ---
    def store_fact(self, entity, attribute, value):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO semantic_memory (entity, attribute, value)
                VALUES (?, ?, ?)
            """, (entity, attribute, value))
            conn.commit()
        return f"Stored fact: {entity}'s {attribute} is {value}"

    def get_facts(self, entity=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if entity:
                cursor.execute("SELECT attribute, value FROM semantic_memory WHERE entity = ?", (entity,))
            else:
                cursor.execute("SELECT entity, attribute, value FROM semantic_memory")
            return cursor.fetchall()

    def delete_fact(self, entity, attribute):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM semantic_memory WHERE entity = ? AND attribute = ?", (entity, attribute))
            conn.commit()
        return f"Forgotten fact: {entity}'s {attribute}."

    def get_full_context(self, user_entity='user', episode_limit=3):
        """
        Retrieves semantic, episodic, and procedural context in a single database connection.
        Optimized to reduce connection overhead for multi-memory retrieval.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Semantic Facts
            cursor.execute("SELECT attribute, value FROM semantic_memory WHERE entity = ?", (user_entity,))
            facts = cursor.fetchall()
            # Episodic Summaries
            cursor.execute("SELECT summary, timestamp FROM episodic_memory ORDER BY timestamp DESC LIMIT ?", (episode_limit,))
            episodes = cursor.fetchall()
            # Procedural Rules
            cursor.execute("SELECT rule_content FROM procedural_memory")
            rules = [row[0] for row in cursor.fetchall()]

            return {
                "facts": facts,
                "episodes": episodes,
                "rules": rules
            }

    # --- Episodic Memory Methods ---
    def _get_embedding(self, text):
        """Generates an embedding for the given text using Ollama."""
        try:
            # Prioritize nomic-embed-text for high-quality embeddings
            model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
            url = f"{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}/api/embeddings"
            # Optimization: Use persistent session to reduce connection overhead
            response = self.session.post(url, json={"model": model, "prompt": text})
            
            if response.status_code != 200:
                # Fallback to main model if nomic is missing
                main_model = os.getenv("OLLAMA_MODEL", "llama3")
                response = self.session.post(url, json={"model": main_model, "prompt": text})
            
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            print(f"[Memory] Embedding error: {e}")
            return None

    def add_episode(self, summary, keywords=""):
        embedding = self._get_embedding(summary)
        vector_blob = np.array(embedding, dtype=np.float32).tobytes() if embedding else None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO episodic_memory (summary, keywords, vector)
                VALUES (?, ?, ?)
            """, (summary, keywords, vector_blob))
            conn.commit()
        return "Episode recorded with semantic embedding."

    def semantic_search(self, query, limit=3):
        """Finds episodes most similar to the query using vectorized cosine similarity."""
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            return self.get_recent_episodes(limit)

        query_vec = np.array(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        
        # Avoid division by zero if query is empty or failed
        if query_norm == 0:
            return self.get_recent_episodes(limit)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT summary, vector, timestamp FROM episodic_memory WHERE vector IS NOT NULL")
            results = cursor.fetchall()

        if not results:
            return []

        # Optimization: Full NumPy vectorization
        # 1. Extract data from SQL results
        summaries = [r[0] for r in results]
        timestamps = [r[2] for r in results]

        # 2. Batch load all vectors into a single matrix
        # Using b''.join is significantly faster than np.vstack in a loop for small blobs
        all_vectors = np.frombuffer(b''.join(r[1] for r in results), dtype=np.float32).reshape(len(results), -1)

        # 3. Calculate dot products and norms in parallel
        dot_products = np.dot(all_vectors, query_vec)
        stored_norms = np.linalg.norm(all_vectors, axis=1)

        # 4. Compute cosine similarities (handle potential zeros)
        # We use np.nan_to_num to treat cases where stored_norm is 0 as similarity 0
        similarities = np.nan_to_num(dot_products / (query_norm * stored_norms))

        # 5. Combine and sort
        scored_results = list(zip(summaries, timestamps, similarities))
        scored_results.sort(key=lambda x: x[2], reverse=True)

        return scored_results[:limit]

    def get_recent_episodes(self, limit=5):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT summary, timestamp FROM episodic_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
            return cursor.fetchall()

    # --- Procedural Memory Methods ---
    def set_rule(self, name, content):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO procedural_memory (rule_name, rule_content)
                VALUES (?, ?)
            """, (name, content))
            conn.commit()
        return f"Rule '{name}' updated."

    def get_all_rules(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT rule_content FROM procedural_memory")
            return [row[0] for row in cursor.fetchall()]

    def delete_rule(self, name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM procedural_memory WHERE rule_name = ?", (name,))
            conn.commit()
        return f"Rule '{name}' has been deleted."

# Global instance
memory = MemoryManager()
