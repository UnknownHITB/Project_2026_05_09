## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Semantic Search & Query Consolidation]
**Learning:** Full NumPy vectorization (using `np.vstack` and matrix multiplication) for cosine similarity is significantly more scalable than row-by-row iteration, providing ~22-31% speedup at 10k items. Additionally, consolidating multiple independent database queries into a single connection (e.g., `get_full_context`) reduces SQLite overhead by ~54-84% per turn.
**Action:** Implement batch vector operations for any similarity-based retrieval. Consolidate frequently co-occurring database lookups into single methods to minimize connection handshakes.
