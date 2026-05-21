## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-20 - [Batching Database Queries & WAL Mode]
**Learning:** Consolidating multiple SQLite queries into a single connection and method (e.g., `get_full_context`) reduced per-turn overhead by ~78% (from 1.82ms to 0.39ms). Enabling WAL mode (`PRAGMA journal_mode=WAL`) significantly improves concurrency and responsiveness for multi-session usage.
**Action:** Always batch related database reads that occur in the same logical turn. Use WAL mode for SQLite databases in web applications.
