## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Similarity Search]
**Learning:** For semantic search involving large numbers of items (e.g., >1000), a fully vectorized NumPy implementation (using matrix multiplication and vectorized norms) is significantly faster than an iterative approach. Joining all vector BLOBs into a single bytes object with `b''.join()` before using `np.frombuffer` and `reshape` is much more efficient than using `np.vstack()` with a list comprehension of small arrays.
**Action:** Prefer vectorized matrix operations over iterative loops for similarity scoring. When building a matrix from many small binary chunks, join the chunks first then create the array to minimize intermediate allocations.
