## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-06-14 - [Database Retrieval Consolidation]
**Learning:** Consolidating multiple sequential database retrieval calls into a single method/connection reduced execution overhead by ~57% (from ~0.7ms to ~0.3ms per turn). Opening/closing connections repeatedly is a significant bottleneck in high-frequency paths like chat turn context injection.
**Action:** Identify sequences of database reads in a single request/turn and consolidate them into a single connection or a specialized batch method.
