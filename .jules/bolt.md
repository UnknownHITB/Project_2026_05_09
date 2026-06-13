## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Similarity Search]
**Learning:** Using `b''.join()` followed by `np.frombuffer().reshape()` is the fastest way to batch-load embeddings from SQLite blobs in this environment, significantly outperforming `np.vstack` with list comprehensions. Full NumPy vectorization (matrix multiplication + vectorized norm calculation) provides measurable scalability (up to ~1.3x speedup for 10k items) compared to iterative row-by-row similarity calculations.
**Action:** Replace iterative vector processing with batch matrix operations when dealing with large datasets. Handle zero-norm edge cases explicitly to maintain stability.
