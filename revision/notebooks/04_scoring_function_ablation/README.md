# NB 04 — Scoring-function (selector) ablation, multi-seed (GPU)

**Why (Reviewer 1 c8, Reviewer 2):** confirm across seeds that **rarity-only** matches the
three-term composite selector, so the decision to make rarity-only the headline is not
single-seed. Runs B2 changing only the neighbor-score weights via env vars.

**Attach:** `brgc-frozen-source`, `brgc-kg-splits`. **Settings:** GPU T4 on; Internet on (first cell).

**Run:** `DATASET_NAME="CoDEx-S"` (cheapest), `SEEDS=[13,42,2025]`, Run All. 7 variants × 3
seeds = 21 runs (~7h; split across sessions — completed runs are skipped).

**Download & send:** `scoring_ablation_<DATASET>.csv`.
