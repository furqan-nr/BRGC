# Notebook 04 — parallel run plan (12 chunks, 3 machines, 4 rounds)

The original `04_scoring_ablation.ipynb` ran the full 7-variant x 3-seed grid for one dataset
at a time. That works for CoDEx-S (~28 min/run, 21 runs ≈ 9.8h — fits one session), but **not**
for CoDEx-M (~220 min/run) or FB15k-237 (~304 min/run), where even the two headline variants
across all seeds would take 22–60+ hours. Those per-run times are measured, not estimated —
taken from the real Notebook-01 B2 runs (`run_complete.json` → `elapsed_min`).

So the task is split into 12 self-contained notebooks ("chunks"), each under 10 hours, each
attaching the same two datasets (`brgc-frozen-source`, `brgc-kg-splits`) and writing its own
CSV whose filename already encodes dataset / variant-set / seed, so you can send me several
finished CSVs at once without collisions.

| # | Notebook | Dataset | Variants | Seed | ~Time |
|---|---|---|---|---|---|
| 1 | `04a_CoDExS_full7_seed13.ipynb` | CoDEx-S | all 7 | 13 | 3.3h |
| 2 | `04a_CoDExS_full7_seed42.ipynb` | CoDEx-S | all 7 | 42 | 3.3h |
| 3 | `04a_CoDExS_full7_seed2025.ipynb` | CoDEx-S | all 7 | 2025 | 3.3h |
| 4 | `04b_CoDExM_headline2_seed13.ipynb` | CoDEx-M | full, rarity_only | 13 | 7.3h |
| 5 | `04b_CoDExM_headline2_seed42.ipynb` | CoDEx-M | full, rarity_only | 42 | 7.3h |
| 6 | `04b_CoDExM_headline2_seed2025.ipynb` | CoDEx-M | full, rarity_only | 2025 | 7.3h |
| 7 | `04c_FB15k237_full_seed13.ipynb` | FB15k-237 | full | 13 | 5.1h |
| 8 | `04c_FB15k237_rarity_only_seed13.ipynb` | FB15k-237 | rarity_only | 13 | 5.1h |
| 9 | `04c_FB15k237_full_seed42.ipynb` | FB15k-237 | full | 42 | 5.1h |
| 10 | `04c_FB15k237_rarity_only_seed42.ipynb` | FB15k-237 | rarity_only | 42 | 5.1h |
| 11 | `04c_FB15k237_full_seed2025.ipynb` | FB15k-237 | full | 2025 | 5.1h |
| 12 | `04c_FB15k237_rarity_only_seed2025.ipynb` | FB15k-237 | rarity_only | 2025 | 5.1h |

**Why CoDEx-M/FB15k-237 only run the two headline variants.** The reviewer concern (R1 c8,
R2) is specifically about whether rarity-only still matches the full composite score once you
leave the single CoDEx-S seed it was first checked on. The other 5 variants (degree_only,
redundancy_only, degree_rarity, degree_redundancy, unscored) are secondary diagnostic detail,
already covered in full on CoDEx-S; repeating all 7 on the two expensive datasets would cost
days of GPU time for marginal additional evidence.

## Suggested rounds (3 machines running together each round)

Pick any 3 chunks per round — grouping by estimated time keeps all three machines finishing
around the same time:

- **Round 1** (~5–7h): #1 (CoDEx-S seed13), #4 (CoDEx-M seed13), #7 (FB15k-237 full seed13)
- **Round 2** (~5–7h): #2 (CoDEx-S seed42), #5 (CoDEx-M seed42), #8 (FB15k-237 rarity seed13)
- **Round 3** (~5–7h): #3 (CoDEx-S seed2025), #6 (CoDEx-M seed2025), #9 (FB15k-237 full seed42)
- **Round 4** (~5h): #10 (FB15k-237 rarity seed42), #11 (FB15k-237 full seed2025), #12 (FB15k-237 rarity seed2025)

Four rounds of three gets through all 12 chunks. Reorder freely — the only real constraint is
not putting two FB15k-237 chunks that total >10h on the same machine in one session, and
watching each Kaggle account's ~30 GPU-hour/week quota (a CoDEx-M or FB15k-237-heavy round can
burn 15–22 GPU-hours across 3 machines, so you may want to spread rounds across more than one
week if you're running everything on only 2–3 accounts).

## After all 12 finish

Send me every `scoring_ablation_*.csv` you have (doesn't need to be all at once — I can fold
them in incrementally as rounds complete). I'll merge them, compute mean±std per variant per
dataset, and confirm (or flag) whether rarity-only still matches full on CoDEx-M and
FB15k-237, the way it already does on CoDEx-S.
