## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-15 - [Vectorized Semantic Search & SQLite WAL]
**Learning:** Vectorizing semantic similarity calculations using NumPy (batch loading with b''.join() + matrix multiplication) provides a significant speedup (~1.5x for 5,000 items) compared to iterative Python loops. Additionally, enabling SQLite WAL mode is essential for maintaining responsiveness in applications with concurrent read/write access.
**Action:** Always prefer NumPy matrix operations over Python loops for vector similarity tasks. Use WAL mode for SQLite databases in multi-threaded or async environments.
