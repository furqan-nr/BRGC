# Revision materials (v1.1.0)

Code and results added for the major revision of COMPJ-2026-07-0954,
"How Much Graph Context Does Relation Prediction Need?" (The Computer Journal).

| Folder | Contents |
|---|---|
| `notebooks/01_neural_perquery_ranks` | Re-runs B0, B2, H_ONLY (3 seeds) and stores per-query test ranks |
| `notebooks/02_significance_and_grouping` | Paired bootstrap CIs and endpoint-uncertainty grouping (CPU) |
| `notebooks/03_embedding_baselines` | TransE, RotatE, CompGCN (PyKEEN) evaluated on relation prediction |
| `notebooks/04_scoring_function_ablation` | Selector ablation, 3 seeds, split into chunks of under 10 h |
| `notebooks/05_schema_ablation` | Schema ablation on FB15k-237, seeds 13 and 2025 (seed 42 in `main_results`) |
| `notebooks/06_dataset_bias_analysis` | Structural diagnostics of the training graphs (CPU) |
| `frozen_source_revision/` | Source used for the revision runs (see below) |
| `per_query_ranks/` | Per-query filtered/raw ranks and test metrics from notebook 01 |
| `result_tables/` | All result CSVs reported in the revised paper |
| `scripts/` | Figure 3 script |

## `frozen_source_revision` vs `../frozen_source`

`data_loader.py` and `model.py` are identical. `config.py`, `train.py` and `utils.py` add only:

- environment overrides for the selector weights and schema flags (`KGC_W_DEGREE`, `KGC_W_REL_RARITY`, `KGC_W_REDUNDANCY`, `KGC_USE_SCHEMA_TOKENS`, `KGC_USE_SCHEMA_PRIOR`), whose defaults equal the original values;
- an optional per-query rank dump at test time (`KGC_DUMP_PERQUERY=1`).

With no environment variables set, the revision source behaves exactly like the original.

## Running

Notebooks are written for Kaggle (T4 GPU) and list the inputs they need at the top. Benchmark
splits are not redistributed. See `../kg/README.md` for download links.
