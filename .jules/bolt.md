## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-06-27 - [Semantic Search Vectorization]
**Learning:** For datasets larger than ~1,000 items, replacing iterative similarity loops with NumPy matrix operations (`matrix @ query_vec`) and vectorized norm calculations provides a significant speedup (~1.5x for 5k items). Using `b''.join()` to batch-load blobs into a single NumPy buffer is significantly faster than iterative `np.frombuffer` calls.
**Action:** Prioritize matrix-level operations for any similarity or embedding-related search logic.
