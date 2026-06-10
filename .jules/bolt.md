## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Semantic Search]
**Learning:** Full NumPy vectorization of cosine similarity (batch loading via `b"".join` and `np.frombuffer`, followed by matrix multiplication) is significantly more scalable than iterative row-by-row processing. It reduces Python loop overhead and leverages BLAS for matrix operations.
**Action:** When performing similarity searches or bulk mathematical operations on data stored in SQLite, prefer loading all vectors into a single NumPy matrix for batch processing rather than iterating over rows.
