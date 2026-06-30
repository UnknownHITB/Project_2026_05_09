## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Semantic Search & WAL Mode]
**Learning:** Full NumPy vectorization (matrix-vector multiplication) for semantic search provides a significant speedup (~1.35x for 5,000 items) compared to iterative approaches. Additionally, enabling SQLite Write-Ahead Logging (WAL) improves concurrency for memory operations.
**Action:** Replace iterative vector operations with NumPy matrix operations when dealing with collections of embeddings. Enable WAL mode for all SQLite databases in the application.
