## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-20 - [SQLite Batching & WAL Mode]
**Learning:** Consolidating multiple SQLite queries into a single connection/method reduces per-turn retrieval overhead by ~60% (from ~0.65ms to ~0.25ms). Enabling WAL mode (`PRAGMA journal_mode=WAL`) is essential for concurrent performance in FastAPI applications where multiple sessions might access the memory database simultaneously.
**Action:** Batch database operations that occur sequentially. Always enable WAL mode for SQLite in multi-user/multi-threaded environments.
