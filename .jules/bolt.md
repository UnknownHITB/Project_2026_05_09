## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Vectorized Semantic Search]
**Learning:** Using `b"".join()` and `np.frombuffer()` to bulk load vectors into a NumPy matrix followed by matrix-vector multiplication provides a measurable speedup (~1.3x for 5k items) over iterative dot product calculations. It leverages NumPy's internal C-optimized loops and reduces Python-level overhead.
**Action:** Prefer vectorized matrix operations over iterative loops when performing similarity searches or other bulk numerical computations.
