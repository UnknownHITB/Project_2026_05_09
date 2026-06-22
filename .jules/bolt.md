## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-22 - [Consolidated Database Retrieval]
**Learning:** Consolidating multiple sequential SQLite queries into a single connection/method reduces retrieval overhead by ~55% (2.23x speedup) in this architecture. This is particularly effective for per-turn context injection where latency is critical.
**Action:** Identify patterns where multiple  blocks are used for a single logical operation and batch them into a single connection.

## 2025-05-22 - [Consolidated Database Retrieval]
**Learning:** Consolidating multiple sequential SQLite queries into a single connection/method reduces retrieval overhead by ~55% (2.23x speedup) in this architecture. This is particularly effective for per-turn context injection where latency is critical.
**Action:** Identify patterns where multiple `with sqlite3.connect(...)` blocks are used for a single logical operation and batch them into a single connection.
