# BRGC: Bounded Role-Aware Graph Context for Relation Prediction

Code and training-free analysis scripts for the paper:

> **How Much Graph Context Does Relation Prediction Need?**
> Furqan Nasir, Muhammad Atif Saeed, Saifullah Jan, Haji Gul. *The Computer Journal* (under review), 2026.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23478806.svg)](https://doi.org/10.5281/zenodo.23478806)

Relation prediction on the usual benchmarks scores very high. How much of that
comes from the graph structure, and how much from the two entities alone? The
paper works through that question with two things: a training-free diagnosis
built on relation entropy, and BRGC, a fixed-encoder model that we keep on a
tight leakage leash and use as a measuring instrument rather than a leaderboard
entry. This repository is the code behind those results. Nothing here is a
cleaned-up reimplementation. It is what actually produced the numbers.

## Repository layout

```
BRGC/
├── frozen_source/     Frozen implementation used for every reported run
│   ├── config.py          run configuration
│   ├── data_loader.py     context construction (bounded, role-aware, leakage-controlled)
│   ├── model.py           DistilBERT classifier over the relation vocabulary
│   ├── train.py           training / evaluation entry point
│   ├── utils.py           metrics and helpers
│   └── IMPLEMENTATION_NOTES.md
├── analysis/          Training-free diagnostics (no GPU required)
│   ├── training_free_baselines_and_entropy.py
│   └── bootstrap_confidence_intervals.py
├── kg/                Place downloaded dataset splits here (see kg/README.md)
├── requirements.txt
├── CITATION.cff
├── LICENSE            (MIT)
└── .zenodo.json       Zenodo deposit metadata (authors, ORCIDs, license)
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate    # optional
pip install -r requirements.txt
```

The benchmark splits are not shipped with the repo. Download them and drop them
under `kg/`. The layout is spelled out in [`kg/README.md`](kg/README.md).

## Reproducing the training-free diagnosis (no GPU)

```bash
python analysis/training_free_baselines_and_entropy.py
python analysis/bootstrap_confidence_intervals.py CoDEx-S
python analysis/bootstrap_confidence_intervals.py CoDEx-M
python analysis/bootstrap_confidence_intervals.py FB15k-237
```

This is the part that needs no GPU. The first script runs the parameter-free
endpoint baselines (global majority, global frequency, p(r|h), p(r|t), naive
Bayes) under the same filtered-ranking protocol the paper uses, and prints the
task-difficulty diagnostics alongside them: relation entropy, H(R|H), H(R|T),
top-1-by-endpoint, and the candidate counts. The second wraps those baselines in
95% bootstrap confidence intervals, one dataset per call.

## Reproducing the neural configurations

Pick the context ladder and the one-sided ablations through environment
variables:

```bash
KGC_DATASET=CoDEx-S KGC_EXPERIMENT_ID=B2 KGC_SEED=42 python frozen_source/train.py
```

- `KGC_DATASET` in `{CoDEx-S, CoDEx-M, FB15k-237}`
- `KGC_EXPERIMENT_ID` in `{B0, B1, B2, H_ONLY, T_ONLY}`
- `KGC_SEED` in `{13, 42, 2025}`

Every run drops a `run_config.json` next to its output. It holds the fully
resolved configuration and a code fingerprint, so any number in the paper traces
back to the exact setup that made it. The finer points live in
[`frozen_source/IMPLEMENTATION_NOTES.md`](frozen_source/IMPLEMENTATION_NOTES.md).

## Revision materials (v1.1.0)

The `revision/` folder holds the notebooks, source and results added for the journal revision: paired per-query significance tests, endpoint-uncertainty grouping, TransE/RotatE/CompGCN baselines, three-seed selector and schema ablations, and dataset-bias diagnostics. See [`revision/README.md`](revision/README.md).

## Citing

If the code or its results end up in your own work, please cite the paper and the
archived software release. The details sit in `CITATION.cff`, which GitHub turns
into a "Cite this repository" button. The Zenodo DOI goes in once the first
release is out.

## License

MIT. See [`LICENSE`](LICENSE).
