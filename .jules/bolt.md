## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2026-05-27 - [Vectorized Search & Context Consolidation]
**Learning:** Consolidating multiple database retrieval calls into a single connection via `MemoryManager.get_full_context` reduces per-turn database retrieval overhead by ~84% (benchmarked at ~0.28ms vs ~1.78ms). Additionally, full NumPy vectorization (`np.vstack` and matrix dot products) provides a ~7-12x speedup for semantic search over iterative methods at a scale of 10,000 items.
**Action:** Use consolidated retrieval methods for multi-part context injection and prefer matrix operations over iterative loops for similarity calculations in memory systems.
