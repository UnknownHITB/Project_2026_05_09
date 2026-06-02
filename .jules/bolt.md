## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [SQLite Connection Consolidation]
**Learning:** Consolidating multiple sequential database queries into a single connection/transaction can reduce retrieval overhead by >60% (e.g., from 0.67ms to 0.25ms for 3 simple queries). Additionally, enabling WAL mode (`PRAGMA journal_mode=WAL`) is essential for concurrent read/write performance in SQLite-backed applications.
**Action:** When a function makes multiple sequential calls to the database to build a context object, implement a dedicated "full context" retrieval method to minimize connection handshakes.
