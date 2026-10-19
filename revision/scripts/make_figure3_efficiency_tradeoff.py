"""Regenerate Figure 3 (accuracy-efficiency trade-off) as a vector PDF.
Source: Compiled results/table_main_results_mean_std.csv (mean and sample std over seeds 13, 42, 2025).
x = evaluation throughput (examples/s), y = filtered MRR; error bars = seed std on both axes."""
import sys, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams.update({"pdf.fonttype": 42, "font.family": "DejaVu Sans", "font.size": 8})
csv, out = sys.argv[1], sys.argv[2]
d = pd.read_csv(csv)
cfgs = ["B0", "B1", "B2", "H_ONLY", "T_ONLY"]
names = {"B0": "B0", "B1": "B1", "B2": "B2", "H_ONLY": "H-only", "T_ONLY": "T-only"}
mk = {"B0": "s", "B1": "^", "B2": "o", "H_ONLY": "D", "T_ONLY": "v"}
col = {"B0": "#7f3b08", "B1": "#2c7fb8", "B2": "#1f3b63", "H_ONLY": "#238b45", "T_ONLY": "#9e9ac8"}
# label offsets (points) chosen per dataset so that labels do not overlap
off = {
    "CoDEx-S":  {"B0": (-9, 0, "right"), "B1": (-9, -9, "right"), "B2": (-9, 9, "right"), "H_ONLY": (9, -2, "left"), "T_ONLY": (9, 0, "left")},
    "CoDEx-M":  {"B0": (-9, 0, "right"), "B1": (-9, -9, "right"), "B2": (-9, 9, "right"), "H_ONLY": (9, 8, "left"), "T_ONLY": (9, 0, "left")},
    "FB15k-237": {"B0": (-9, 0, "right"), "B1": (24, 8, "left"), "B2": (24, -10, "left"), "H_ONLY": (9, 5, "left"), "T_ONLY": (9, -9, "left")},
}
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.35))
for ax, ds in zip(axes, ["CoDEx-S", "CoDEx-M", "FB15k-237"]):
    s = d[d.Dataset == ds].set_index("Config")
    for c in cfgs:
        r = s.loc[c]
        ax.errorbar(r.ExamplesPerSecond_mean, r.FilteredMRR_mean, xerr=r.ExamplesPerSecond_std, yerr=r.FilteredMRR_std,
                    fmt=mk[c], color=col[c], ms=5, capsize=2, elinewidth=0.8, label=names[c], zorder=3)
        dx, dy, ha = off[ds][c]
        ax.annotate(names[c], (r.ExamplesPerSecond_mean, r.FilteredMRR_mean), xytext=(dx, dy), textcoords="offset points",
                    ha=ha, va="center", fontsize=7.5,
                    arrowprops=(dict(arrowstyle="-", lw=0.5, color="#555555", shrinkA=0, shrinkB=3) if abs(dx) > 12 or abs(dy) > 12 else None))
    lo = (s.FilteredMRR_mean - s.FilteredMRR_std).min(); hi = (s.FilteredMRR_mean + s.FilteredMRR_std).max()
    pad = (hi - lo) * 0.10
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_xlim(0, 1750)
    ax.set_title(ds, fontsize=9, fontweight="bold")
    ax.set_xlabel("Evaluation examples/s")
    ax.grid(True, ls=":", lw=0.5, color="#999999")
    ax.tick_params(labelsize=7)
axes[0].set_ylabel("Filtered MRR")
fig.tight_layout(w_pad=1.0)
fig.savefig(out)
