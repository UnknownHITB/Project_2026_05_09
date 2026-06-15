## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-22 - [Database Connection Consolidation]
**Learning:** Consolidating multiple sequential database retrieval calls into a single connection reduced execution overhead by ~61% (from ~0.000454s to ~0.000176s per set of queries). In Python/SQLite, connection setup and teardown are significant overheads for high-frequency "get_context" calls used in LLM prompts.
**Action:** Use consolidated retrieval methods for data that is frequently fetched together. Enable SQLite WAL mode to improve concurrency for simultaneous read/write operations.
