## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is create critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-17 - [Consolidated Database Retrieval]
**Learning:** Consolidating multiple SQLite retrieval calls into a single connection significantly reduces overhead (measured ~55% improvement). Opening and closing database connections for every small query within a single turn is a common but avoidable bottleneck.
**Action:** Always look for patterns where multiple database reads are performed sequentially for the same context and consolidate them into a single method or connection.
