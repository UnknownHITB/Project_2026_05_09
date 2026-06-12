## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Full Vectorization & DB WAL Mode]
**Learning:** Full NumPy vectorization (loading all vectors via `b''.join` and `np.frombuffer`) is significantly more scalable than iterative row-by-row similarity calculations. Even when using NumPy inside an iterative loop, the overhead of Python's loop and repeated function calls dominates. Enabling SQLite Write-Ahead Logging (WAL) is a zero-cost win for applications with interleaved reads and writes (like an AI assistant recording memories while searching them).
**Action:** Replace iterative row-processing with matrix-based operations for any similarity or search tasks. Always enable WAL mode for SQLite databases in high-concurrency or real-time assistant contexts.
