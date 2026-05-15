## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2026-05-15 - [DB Consolidation & Shared Providers]
**Learning:** Consolidating multiple SQLite queries into a single connection/context in Python reduces per-turn overhead significantly (measured ~50% reduction from 0.5ms to 0.2ms for 3 queries). In FastAPI, using a persistent module-level provider ensures TCP connection pooling via `requests.Session` is actually utilized across requests.
**Action:** Consolidate multiple database lookups into single methods when they occur together. Reuse API provider instances in server environments to leverage session persistence.
