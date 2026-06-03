## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-20 - [Full Vectorization of Semantic Search]
**Learning:** For semantic search, full NumPy vectorization (batch loading blobs into a matrix and using matrix-vector multiplication) provides a significantly better scaling profile than iterative row-by-row dot products. In this codebase, batching vector conversion from blobs reduced search latency by ~30% for 10,000 items.
**Action:** Replace iterative loops over database results with batch NumPy operations whenever possible, especially for embedding similarity checks.
