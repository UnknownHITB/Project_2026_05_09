## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-20 - [Vectorized Similarity Search]
**Learning:** For medium-scale datasets (~5,000 items), vectorizing similarity calculations using NumPy matrix operations (`b''.join()` + `np.frombuffer().reshape()` + `np.dot()`) is significantly faster than iterative loops in Python. However, the performance gap narrows as the dataset scales to 10,000+ items due to the overhead of joining large buffers in Python 3.12.
**Action:** Use full NumPy vectorization for search tasks but monitor memory usage for very large datasets. Ensure consistent return types (e.g., 3-tuples) across all search paths to avoid caller-side errors.
