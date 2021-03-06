import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns
from common_plot import setup_mpl

colors = sns.color_palette("colorblind")
setup_mpl(1.1)

df_cppe = pd.read_csv("cppe_runs/solvated_50_errors_serial_intel.csv")
df_pelib = pd.read_csv("pelib_data/pelib_errors.csv")

dfs = [df_cppe, df_pelib]
impl = ["CPPE", "PElib"]

fig, axes = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True)
for ii, theta in enumerate([0.2, 0.3, 0.5, 0.7, 0.99]):
    for axcol, exp_order in zip(axes, [3,5,7]):
        for ax, df, im in zip(axcol, dfs, impl):
            err_F_i = df[f"err_F_{theta}_{exp_order}"]
            sns.histplot(x=np.log10(err_F_i), ax=ax, stat="probability", label=fr"$\theta = {theta}$",
                         color=colors[ii], edgecolor="black", linewidth=0.02)
            ax.set_xlabel(r"$\log_{10} F^\mathrm{err}$")
            ax.set_xlim([-10, 0])
            ax.set_title(rf"{im}, $p$ = {exp_order}")
handles, labels = ax.get_legend_handles_labels()
plt.tight_layout()
lgd = fig.legend(handles, labels, loc='upper center', ncol=5, bbox_to_anchor=(0.5, 1.05))
plt.savefig("accuracy_fmm_field.png", dpi=600, bbox_extra_artists=(lgd,), bbox_inches="tight")

