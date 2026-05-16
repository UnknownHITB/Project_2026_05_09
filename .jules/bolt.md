## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-15 - [Database Call Consolidation]
**Learning:** Consolidating multiple database retrieval calls into a single connection via `MemoryManager.get_full_context` reduces per-turn database overhead by approximately 50-60%. Each SQLite connection/transaction has non-negligible overhead, especially when repeated frequently.
**Action:** When multiple related pieces of data are needed from the same database, provide a consolidated retrieval method to minimize connection and transaction overhead.
