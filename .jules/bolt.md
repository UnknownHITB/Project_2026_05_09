## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [NumPy Vectorization for Semantic Search]
**Learning:** Replacing iterative row-by-row cosine similarity calculations with full NumPy vectorization (using `np.vstack` and matrix multiplication) provides a significant performance boost (~33% for 5,000 items) and improves scalability.
**Action:** Favor batch processing and matrix operations over Python loops when performing mathematical computations on large datasets.
