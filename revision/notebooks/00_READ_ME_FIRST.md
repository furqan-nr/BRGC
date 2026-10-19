# BRGC Revision Experiments — Kaggle run kit

This folder contains everything needed to produce the **GPU experiments** that the four
Computer Journal reviewers asked for. Each notebook is self-contained, matches the frozen
BRGC pipeline so results merge with the existing tables, and is sized for **free Kaggle**
(12-hour sessions, ~30 GPU-hours/week, T4 GPU).

The text/reframing/formatting fixes do **not** need any of these runs — I handle those in
the manuscript. These notebooks only produce the numbers that genuinely require a GPU (or,
for two of them, a few minutes of CPU).

---

## Step 0 — Upload the two shared Kaggle Datasets (once)

Under `kaggle_datasets/` there are two folders. Upload each as a Kaggle Dataset
(Kaggle → Datasets → New Dataset → upload the folder). You only do this once; every
notebook attaches them.

| Upload this folder | Suggested dataset name | Contains |
|---|---|---|
| `kaggle_datasets/brgc_kg_splits` | `brgc-kg-splits` | `CoDEx-S/`, `CoDEx-M/`, `FB15k-237/` each with `train.txt`, `valid.txt`, `test.txt` |
| `kaggle_datasets/brgc_frozen_source` | `brgc-frozen-source` | `frozen_source/` — the five BRGC `.py` files (patched to dump per-query ranks and to accept selector/schema overrides; defaults unchanged) |

The notebooks auto-find these under `/kaggle/input`, so the exact dataset slug name does
not matter.

---

## The notebooks (run in any order; priority marked)

| # | Notebook | GPU? | Addresses | Output to send me |
|---|----------|------|-----------|-------------------|
| 01 | `01_neural_perquery_ranks` | **GPU** | per-query ranks for the significance test + grouping | `BRGC_perquery_<DATASET>.zip` |
| 02 | `02_significance_and_grouping` | CPU | **Reviewers 2/3/4** paired MRR-difference CIs; **Reviewer 3 c1** context-gain by endpoint uncertainty | `paired_significance.csv`, `endpoint_uncertainty_grouping.csv` |
| 03 | `03_embedding_baselines` | **GPU** | **Reviewer 1 c6** are TransE/RotatE/CompGCN also endpoint-dominated? | `kge_relation_prediction_<DATASET>.csv` |
| 04 | `04_scoring_function_ablation` | **GPU** | **Reviewer 1 c8 / Reviewer 2** justify rarity-only selector across seeds | `scoring_ablation_<DATASET>.csv` |
| 05 | `05_schema_ablation` | **GPU** | **Reviewer 3 / Reviewer 2** multi-seed schema ablation (seeds 13, 2025) | `schema_ablation_multiseed_<DATASET>.csv` |
| 06 | `06_dataset_bias_analysis` | CPU | **Reviewer 1 Q2 / Reviewer 3 c2** *why* p(r\|t) is strong | `dataset_bias_diagnostics.csv` |

**Highest value first:** 01 → 02 (the significance test is the single most-requested fix),
then 03 (embedding baselines), then 04, 06, and 05 last. 02 and 06 are CPU and take minutes.

---

## Priority and time budget (free Kaggle: 12h/session, ~30h/week)

| Notebook | Per-dataset cost (T4) | How to batch |
|---|---|---|
| 01 | CoDEx-S ~1.5h · CoDEx-M ~5h · FB15k-237 ~9–11h | one dataset per session; for FB15k-237 run `SEEDS=[42]` then `[13,2025]` |
| 02 | minutes (CPU) | run once after 01 finishes for all datasets |
| 03 | CoDEx ~0.5–1h · FB15k-237 ~1–2h per model | one dataset per session; drop CompGCN if tight |
| 04 | CoDEx-S ~20 min/run × 21 runs ≈ 7h | one or two sessions |
| 05 | FB15k-237 ~4–6h/run × 8 runs | 1–2 runs per session across the week |
| 06 | seconds (CPU) | anytime |

Every notebook **skips already-completed runs**, so you can stop and resume across sessions.
After each session, run the final cell and **download the artifact zip/CSV**; keep every one
and send them to me.

---

## General Kaggle settings for the GPU notebooks

1. Open the notebook: Kaggle → Code → New Notebook → File → Import Notebook.
2. Right panel → **Add Input** → add `brgc-kg-splits` (and `brgc-frozen-source` for 01/04/05).
3. Settings: **Accelerator = GPU T4**, **Internet = On** (only the first cell needs it, to
   fetch DistilBERT; after that it runs offline).
4. Edit the `DATASET_NAME` / `SEEDS` cell for the session, then **Run All**.

Each notebook's own `README.md` lists exactly what to attach and the resulting
`/kaggle/input` paths.

---

## What I do with the outputs

You send the zips/CSVs; I merge them into the manuscript: the paired CIs replace the
"statistically reliable" wording with proper significance statements, the grouping table
answers Reviewer 3's comment 1 directly, the embedding baselines become a new comparison
row, the multi-seed ablations upgrade the single-seed caveats, and the dataset-bias table
turns Reviewer 1's Q2 into a concrete explanation. Anything you choose **not** to run, I
reframe as a stated limitation (every reviewer allowed that fallback).
