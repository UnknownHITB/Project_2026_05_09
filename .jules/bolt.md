## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [SQLite Connection Consolidation]
**Learning:** Sequential database queries that open/close their own connections incur significant overhead (~0.45ms vs ~0.17ms per set). Consolidating these into a single "full context" retrieval method reduces latency by ~61% for repeated state-loading operations.
**Action:** Identify patterns where multiple `with sqlite3.connect(...)` blocks are used in the same request/turn lifecycle and merge them into a single connection.
