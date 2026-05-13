## 2026-05-09 - Faster RMS Calculation for VAD
**Learning:** Manual calculation of RMS using `struct.unpack` and a Python loop is extremely slow (~50x slower) compared to the built-in `audioop.rms` function. In voice activity detection (VAD), where every chunk must be processed in real-time, this overhead can be significant.
**Action:** Always prefer built-in modules like `audioop` for audio processing tasks before resorting to manual implementation or even NumPy for small buffers. Note: `audioop` is deprecated in Python 3.13, so for future-proofing, an alternative like NumPy or a C extension might be needed eventually.

## 2026-05-13 - API Session & Search Optimization
**Learning:** Using a persistent `requests.Session` for Ollama API calls reduces TCP handshake latency significantly for multi-turn chats and tool-calling. In semantic search, hoisting the query vector norm calculation out of the loop provides a ~40-60% speedup on similarity searches without adding complexity.
**Action:** Always implement session pooling for frequent API interactions and profile loop-internal math for hoistable constants.
