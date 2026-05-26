## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-26 - [Database Connection Consolidation]
**Learning:** Consolidating multiple SQLite retrieval calls into a single method/connection reduces per-turn retrieval overhead by ~84% (from ~1.7ms to ~0.28ms). While SQLite is fast, the overhead of repeated `connect()` calls in a high-frequency loop (like LLM context injection) is significant. Enabling WAL mode (`PRAGMA journal_mode=WAL`) further improves concurrency for multi-threaded access.
**Action:** Always look for patterns where multiple database calls are made in sequence and consolidate them into a single connection scope.
