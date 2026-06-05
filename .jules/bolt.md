## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Similarity Search]
**Learning:** Full NumPy vectorization (matrix multiplication + batch norms) is significantly faster than row-by-row iteration for similarity search, especially as the dataset grows. Consolidating SQLite blobs via `b''.join()` followed by a single `np.frombuffer` call is a high-performance way to bridge the database-to-matrix gap.
**Action:** When performing searches or bulk calculations on embeddings, avoid Python loops. Use matrix operations to leverage NumPy's underlying C/Fortran optimizations.
