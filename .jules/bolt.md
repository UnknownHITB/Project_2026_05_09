## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [SQLite Query Consolidation]
**Learning:** Consolidating multiple sequential database queries into a single connection reduced execution overhead by ~57% (from ~0.00062s to ~0.00027s per turn). The overhead of opening/closing SQLite connections is significant when done multiple times per LLM turn.
**Action:** Use consolidated retrieval methods to fetch all necessary state (facts, history, rules) in a single database session.
