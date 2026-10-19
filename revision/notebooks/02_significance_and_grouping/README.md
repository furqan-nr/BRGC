# NB 02 — Paired significance + endpoint grouping (CPU, no GPU)

**Why:** turns NB 01's per-query ranks into the statistics reviewers asked for —
paired bootstrap 95% CIs for MRR differences (B2−B0, B2−H_ONLY, B0−best baseline) and
context gain grouped by tail ambiguity (Reviewer 3, comment 1).

**Attach:**
- `brgc-kg-splits`
- your **NB 01 outputs**: unzip the `BRGC_perquery_<DATASET>.zip` files and upload them as a
  Kaggle Dataset (any name). The notebook auto-finds every `per_query_ranks.npz`.

**Settings:** CPU is fine (no GPU). Runs in minutes. You can also run it locally.

**Download & send:** `paired_significance.csv`, `endpoint_uncertainty_grouping.csv`.
