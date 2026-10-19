# NB 05 — Schema ablation, multi-seed (GPU)

**Why (Reviewer 3, Reviewer 2):** the schema ablation (S0/S1/S2/S3) was FB15k-237 seed 42
only. This adds seeds 13 and 2025 so it is no longer single-seed.

**Attach:** `brgc-frozen-source`, `brgc-kg-splits`. **Settings:** GPU T4 on; Internet on (first cell).

**Run:** `DATASET_NAME="FB15k-237"`, `SEEDS=[13,2025]`, Run All. 4 variants × 2 seeds = 8
runs at ~4–6h each — do 1–2 runs per 12h session across the week (completed runs skipped).

**Download & send:** `schema_ablation_multiseed_<DATASET>.csv` (I merge with the seed-42 row).
