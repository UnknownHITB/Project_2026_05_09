## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2026-06-26 - [Vectorized Semantic Search]
**Learning:** For semantic search, full NumPy vectorization (batch loading + matrix ops) provides a measurable speedup over iterative methods as the dataset scales. Using `b''.join()` followed by `np.frombuffer().reshape()` is a faster technique for bulk loading embeddings than iterative `np.frombuffer()` calls or `np.vstack()` with list comprehensions.
**Action:** Replace iterative calculations in numerical loops with vectorized NumPy operations. Use efficient batch-loading patterns for binary blobs from databases.
