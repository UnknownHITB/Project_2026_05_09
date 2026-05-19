## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Consolidated DB Retrieval & Provider Singleton]
**Learning:** Batching multiple independent SQLite lookups (semantic, episodic, procedural) into a single connection significantly reduces I/O overhead. Implementing a singleton for the LLM provider ensures that the persistent `requests.Session` is shared across all session handlers, maximizing TCP connection pooling.
**Action:** Identify repeated per-turn database lookups and consolidate them into a single retrieval method. Ensure provider instances are cached when they manage expensive resources like network sessions or model handles.
