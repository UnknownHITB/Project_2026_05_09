## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2026-05-20 - [Consolidated Database Connections]
**Learning:** Consolidating multiple SQLite database retrieval calls into a single connection significantly reduces per-turn overhead in chat assistants. Opening and closing connections for each query is expensive compared to the query execution time for small datasets like session memory or system rules.
**Action:** When multiple database queries are required for a single logical operation (e.g., prompt construction), use a single connection/context manager to perform all retrievals.
