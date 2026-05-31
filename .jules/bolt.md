## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Similarity Search]
**Learning:** For semantic search with embeddings, replacing a Python row-by-row loop with full NumPy vectorization (matrix multiplication and batch norm) provides a significant speedup as the memory size grows. Benchmarking with 10k items showed a ~31% improvement (0.206s -> 0.142s) in pure calculation time.
**Action:** Use `np.vstack` and batch operations for similarity calculations instead of iterating over rows.
