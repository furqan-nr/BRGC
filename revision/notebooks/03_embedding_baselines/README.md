# NB 03 — Embedding baselines TransE / RotatE / CompGCN (GPU)

**Why (Reviewer 1, comment 6):** show whether classic embedding/GNN models are *also*
endpoint-dominated on these benchmarks, evaluated on relation prediction (h,?,t) under the
same filtered ranking.

**Attach:** `brgc-kg-splits`. **Settings:** GPU T4 on; Internet on (installs PyKEEN).

**Run:** set `DATASET_NAME` and `MODELS` (drop `CompGCN` if a session is tight), Run All.
One dataset per session.

**Download & send:** `kge_relation_prediction_<DATASET>.csv`.
