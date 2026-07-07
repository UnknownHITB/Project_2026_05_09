## 2025-05-15 - [Semantic Search & Connection Pooling]
**Learning:** Hoisting vector norm calculations out of loops in Python/NumPy provides a measurable speedup (e.g., ~33% for 10k items) because it reduces redundant scalar operations and function call overhead. Additionally, using `requests.Session()` for local LLM APIs (like Ollama) is critical to avoid TCP handshake latency in multi-turn chat and embedding generation.
**Action:** Always check for redundant calculations in loops that involve NumPy or math operations. Ensure API clients use persistent sessions for repeated calls to the same host.

## 2025-05-16 - [Singleton Provider in Server]
**Learning:** In stateless HTTP servers (like FastAPI), helper functions that instantiate providers on every request negate any internal caching or connection pooling (like `requests.Session`). Caching these as singletons at the module level is a high-impact, low-risk win.
**Action:** Identify helper functions that create new instances of providers or API clients and convert them to singleton patterns.
