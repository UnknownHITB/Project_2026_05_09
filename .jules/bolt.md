## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2026-06-17 - [Database Connection Consolidation]
**Learning:** Consolidating multiple sequential database queries into a single connection significantly reduces execution overhead (by ~57% in this case). Even for lightweight SQLite databases, the cumulative cost of opening and closing connections across multiple utility methods adds measurable latency to high-frequency code paths like LLM prompt construction.
**Action:** Look for patterns where multiple `with sqlite3.connect(...)` blocks are executed in sequence. Consolidate them into a single connection when they share the same execution context.
