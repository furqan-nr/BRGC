# Notebook 05 — parallel run plan (8 chunks, accounts with 5h / 6h / 7h remaining)

8 single-run chunks: 4 schema variants (S0_context_only, S1_schema_tokens, S2_schema_prior,
S3_full_schema) x 2 new seeds (13, 2025) — seed 42 is already in the paper. Each run is
**~5.07 hours**, measured from the real Notebook-01 FB15k-237 B2 run (`run_complete.json` →
`elapsed_min` = 304.4). That number is fixed by the dataset and model, not by which account
runs it, so it's the number to check your remaining quota against every round.

## This round: 5h / 6h / 7h remaining

| Account (remaining quota) | Safe to run a chunk now? | Why |
|---|---|---|
| 5h | **No — skip this round.** | A run needs ~5.07h; you have less than that. Kaggle kills the session before `train.py` finishes, the run produces no `test_metrics.json`/CSV, and the quota you spent is gone with nothing to show for it. Don't start one. |
| 6h | **Yes, but tight (~0.93h buffer).** | ~5.07h measured elsewhere; real runs vary a bit by GPU/instance, so this is lower-risk than the 5h account but not risk-free. Pick ONE chunk, don't try to queue a second after it. |
| 7h | **Yes, comfortable (~1.93h buffer).** | Safest of the three this round. |

**This round's assignment (2 of 8 chunks):**
- 7h account → `05_FB15k237_S0_context_only_seed13.ipynb`
- 6h account → `05_FB15k237_S1_schema_tokens_seed13.ipynb`
- 5h account → sits out this round (nothing else in this project currently needs <5h of GPU
  time; either wait for this account's weekly quota to reset, or lend it to whichever of the
  other two machines needs a second run once quotas refresh).

## Remaining chunks for future rounds

Once quotas reset (typically weekly on Kaggle), repeat with whichever accounts have ≥5.5h
free, picking the next unrun chunk in this order:

1. ~~`05_FB15k237_S0_context_only_seed13.ipynb`~~ — DONE (received)
2. ~~`05_FB15k237_S1_schema_tokens_seed13.ipynb`~~ — DONE (received)
3. `05_FB15k237_S2_schema_prior_seed13.ipynb`
4. `05_FB15k237_S3_full_schema_seed13.ipynb`
5. `05_FB15k237_S0_context_only_seed2025.ipynb`
6. `05_FB15k237_S1_schema_tokens_seed2025.ipynb`
7. `05_FB15k237_S2_schema_prior_seed2025.ipynb`
8. `05_FB15k237_S3_full_schema_seed2025.ipynb`

With a full ~30h/week quota per account (the normal case once reset), each account can
comfortably do 2–5 of these per week, so all 8 should clear within one more round once quotas
are back to normal — this 5h/6h/7h round is just unusually constrained.

## After all 8 finish

Send me every `schema_ablation_FB15k-237_*.csv` you have, whenever you have them — I don't
need all 8 at once. I'll merge them with the existing seed-42 row and update the schema
ablation table (currently flagged `[In progress]` in the response letter) to a proper 3-seed
result.
