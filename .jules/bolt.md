## 2026-05-09 - Faster RMS Calculation for VAD
**Learning:** Manual calculation of RMS using `struct.unpack` and a Python loop is extremely slow (~50x slower) compared to the built-in `audioop.rms` function. In voice activity detection (VAD), where every chunk must be processed in real-time, this overhead can be significant.
**Action:** Always prefer built-in modules like `audioop` for audio processing tasks before resorting to manual implementation or even NumPy for small buffers. Note: `audioop` is deprecated in Python 3.13, so for future-proofing, an alternative like NumPy or a C extension might be needed eventually.

## 2026-05-10 - Efficient Memory Context Retrieval
**Learning:** Multiple separate database connections and queries to fetch different memory types (semantic, episodic, procedural) for every LLM turn adds significant latency and overhead. Additionally, repeated TCP handshakes for local API calls (Ollama) add up.
**Action:** Consolidate multiple related database queries into a single connection or method. Use `requests.Session()` to enable HTTP Keep-Alive and connection pooling, especially for local AI providers where multiple calls (embeddings + chat) are common.
