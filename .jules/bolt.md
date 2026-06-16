## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-06-16 - [Database Query Consolidation]
**Learning:** Consolidating three sequential database queries (Facts, Episodes, Rules) into a single SQLite connection reduced execution overhead by ~61% (from 0.00045s to 0.00017s per turn). Opening/closing connections in a tight loop (like per-chat-turn context injection) is a significant bottleneck.
**Action:** Look for patterns where multiple retrieval methods are called on the same data source and provide a batch retrieval method.
