## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Similarity Search]
**Learning:** For semantic search, moving from an iterative loop to a fully vectorized NumPy implementation (using `np.frombuffer` on a joined byte stream of vectors) provides a massive speedup (often >10x) by leveraging BLAS/LAPACK optimizations. However, joining thousands of blobs into a single byte string can occasionally have overhead that slightly reduces the gain in specific Python 3.12 environments, but it remains the superior approach for scalability.
**Action:** Use matrix-vector operations instead of loops whenever processing a collection of embeddings.
