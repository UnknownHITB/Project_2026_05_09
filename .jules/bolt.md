## 2025-05-24 - [Vectorized Similarity & Consolidated DB Hits]
**Learning:** Vectorizing cosine similarity with NumPy matrix operations (`np.dot` on a matrix vs loop) provides a massive speedup as memory grows (measured ~40% gain at 1000 items). Consolidating multiple SQLite reads into a single connection/transaction reduces per-turn overhead by avoiding repeated WAL check-pointing and connection setup latency.
**Action:** Use matrix-vector operations for any semantic search or similarity tasks. Batch database reads that occur during the same request cycle into a single connection handler.
