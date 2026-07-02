## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Semantic Search]
**Learning:** For datasets larger than a few hundred items, vectorizing cosine similarity using NumPy matrix-vector multiplication is significantly faster than iterative loops. Using `b"".join()` to concatenate BLOBs before loading them into a NumPy array with `np.frombuffer()` is an efficient way to bulk-load embeddings from SQLite.
**Action:** Use NumPy vectorization for any operation involving more than 1000 vectors. Ensure all return paths in search functions maintain consistent tuple structures.
