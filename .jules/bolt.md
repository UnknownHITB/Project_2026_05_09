## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2024-05-20 - [Vectorized Similarity Search]
**Learning:** For semantic search, full NumPy vectorization (bulk loading via b''.join, matrix multiplication, and vectorized norm calculation) provides a measurable speedup (~20-30%) over iterative methods as the dataset scales. Batch loading vectors from blobs using `np.frombuffer` on a joined byte string is particularly efficient.
**Action:** Always prefer batch/matrix operations over element-wise loops for numerical computations involving embeddings.
