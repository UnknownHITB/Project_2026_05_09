## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-22 - [Vectorized Semantic Search]
**Learning:** Full NumPy vectorization (batch loading vectors from SQLite blobs, matrix multiplication, and vectorized norm calculation) provides a significant speedup (approx. 2x - 4x) for semantic search compared to iterative row-by-row processing, especially as the number of memory entries grows.
**Action:** Always prefer vectorized operations over Python loops for similarity calculations or any operations involving large sets of embeddings.
