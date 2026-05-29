## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-20 - [Database Connection Consolidation]
**Learning:** Consolidating multiple SQLite database retrieval calls into a single connection significantly reduces per-turn overhead (by ~54-84%). Opening and closing connections is expensive in high-frequency loops like an LLM chat agent's context injection.
**Action:** Always look for patterns where multiple  calls are used to gather data for the same logical operation and consolidate them.

## 2025-05-20 - [Database Connection Consolidation]
**Learning:** Consolidating multiple SQLite database retrieval calls into a single connection significantly reduces per-turn overhead (by ~54-84%). Opening and closing connections is expensive in high-frequency loops like an LLM chat agent's context injection.
**Action:** Always look for patterns where multiple `with sqlite3.connect()` calls are used to gather data for the same logical operation and consolidate them.
