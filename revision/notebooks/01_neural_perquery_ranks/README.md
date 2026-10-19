# NB 01 — Neural per-query ranks (GPU)

**Why:** the original runs saved only aggregate metrics. The paired significance tests
(NB 02) and the endpoint-uncertainty grouping (NB 02) need the **per-query filtered ranks**,
which this notebook regenerates by re-running B0, B2, H_ONLY and dumping them.

**Attach (Add Input):**
- `brgc-frozen-source`  → appears at `/kaggle/input/<slug>/frozen_source/*.py`
- `brgc-kg-splits`      → appears at `/kaggle/input/<slug>/{CoDEx-S,CoDEx-M,FB15k-237}/`

**Settings:** GPU T4 on; Internet on (first cell only).

**Run:** set `DATASET_NAME` (one per session) and `SEEDS`, then Run All. For FB15k-237,
if a session risks >12h, run `SEEDS=[42]` first, then `[13,2025]` next session.

**Download & send:** `BRGC_perquery_<DATASET>.zip` (contains `per_query_ranks.npz` per
config/seed + `test.txt`). Run for all three datasets.
