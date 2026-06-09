## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2026-06-09 - [SQLite Connection Consolidation]
**Learning:** Consolidating multiple sequential database queries into a single connection reduced execution overhead by ~61% (from ~1.13ms to ~0.46ms per set of queries). Opening/closing SQLite connections frequently adds measurable latency due to file system locking and initialization.
**Action:** When multiple database queries are performed in the same logical operation (e.g., building a prompt context), group them into a single connection block.
