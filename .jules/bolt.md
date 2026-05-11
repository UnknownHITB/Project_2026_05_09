## 2026-05-09 - Faster RMS Calculation for VAD
**Learning:** Manual calculation of RMS using `struct.unpack` and a Python loop is extremely slow (~50x slower) compared to the built-in `audioop.rms` function. In voice activity detection (VAD), where every chunk must be processed in real-time, this overhead can be significant.
**Action:** Always prefer built-in modules like `audioop` for audio processing tasks before resorting to manual implementation or even NumPy for small buffers. Note: `audioop` is deprecated in Python 3.13, so for future-proofing, an alternative like NumPy or a C extension might be needed eventually.

## 2026-05-10 - Efficient Loop Hoisting for Vector Similarity
**Learning:** For semantic search using cosine similarity, hoisting vector norm calculations out of loops provides a measurable speedup (~30% for small to medium datasets). While full NumPy vectorization (e.g., `np.vstack`) is more efficient for very large datasets (>5,000 items), the overhead of creating large matrices can make simple loop hoisting faster for typical "personal" memory sizes.
**Action:** Identify and hoist redundant calculations out of loops in performance-critical paths, especially those involving expensive math operations like `np.linalg.norm`.
