## 2026-05-09 - Faster RMS Calculation for VAD
**Learning:** Manual calculation of RMS using `struct.unpack` and a Python loop is extremely slow (~50x slower) compared to the built-in `audioop.rms` function. In voice activity detection (VAD), where every chunk must be processed in real-time, this overhead can be significant.
**Action:** Always prefer built-in modules like `audioop` for audio processing tasks before resorting to manual implementation or even NumPy for small buffers. Note: `audioop` is deprecated in Python 3.13, so for future-proofing, an alternative like NumPy or a C extension might be needed eventually.

## 2026-05-12 - Vector Norm Hoisting for Semantic Search
**Learning:** Recalculating the norm of a query vector within a loop for cosine similarity is a common O(n) bottleneck. In Python/NumPy, hoisting this (d)$ operation outside the loop provides a significant speedup (~30% for 1000 items) by avoiding redundant calculations.
**Action:** Always check similarity loops for invariant calculations that can be hoisted.
