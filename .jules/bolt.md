## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Semantic Search]
**Learning:** Full NumPy vectorization (using `np.frombuffer` on joined bytes to build a matrix and `np.dot` for similarity) is significantly faster (approx. 2.8x-4.4x) than row-by-row iteration in Python, even with individual NumPy operations inside the loop. `np.argsort` also provides an efficient way to rank results without Python-level sorting.
**Action:** Prefer matrix-based operations over iterative row processing for all vector-related tasks in memory or search systems.
