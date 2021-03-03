import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from scipy import constants

from common_plot import setup_mpl

setup_mpl(1.3)

eV = constants.value("Hartree energy in eV")

shell = 50

adc_direct = pd.read_csv(f"cppe_runs/adc_direct_{shell}.csv")
adc_direct["scheme"] = "direct"

all_dfs = []

errors = ["excitation_energy", "oscillator_strength"]
for ii, theta in enumerate([0.2, 0.3, 0.5, 0.7, 0.99]):
    for exp_order in [3, 5, 7]:
        dfa = pd.read_csv(f"cppe_runs/adc_{shell}_{theta}_{exp_order}.csv")
        dfa["scheme"] = "fmm"
        dfa["theta"] = theta
        dfa["exporder"] = exp_order
        
        for e in errors:
            ee = e.replace("_", "-")
            dfa[f"error-{ee}"] = np.abs(dfa[e] - adc_direct[e])
        all_dfs.append(dfa)

df = pd.concat(all_dfs, ignore_index=True)

df_pelib = pd.read_csv("pelib_data/excitation_energy_accuracy.tsv", sep="\t")
nr = df_pelib.shape[0] // 5

df_pelib['excitation'] = np.tile(np.arange(5), nr)
df_pelib['error-excitation-energy'] = np.abs(df_pelib['error'])
df_pelib['exporder'] = df_pelib['order']
df_pelib['method'] = "PE-TDDFT"

df["error-excitation-energy"] *= eV
df["method"] = "PE-ADC(2)"

print(df.describe())
print(df_pelib.describe())

sns.set_context("poster")

df = pd.concat([df, ], ignore_index=True)
df = pd.concat([df, df_pelib], ignore_index=True)

g = sns.catplot(x="excitation", y="error-excitation-energy", hue="theta", kind="bar",
                col="exporder", row='method', data=df, log=False, sharey="row", legend=False,
                margin_titles=True, palette="colorblind", saturation=0.9)

xtx = [rf"S$_{i}$" for i in range(1, 6)]
(g.set_axis_labels("", r"$|E_\mathrm{direct} - E_\mathrm{FMM}|$ [eV]")
.set_xticklabels(xtx)
.set_titles(col_template=r"$p = {col_name}$", row_template = '{row_name}')
.set(yscale="log", ylim=(1e-7, 1e-1))
)

plt.tight_layout()
g.axes[0, 1].legend()

handles, labels = g.axes[0, 1].get_legend_handles_labels()
labels = [rf"$\theta$ = {x}" for x in labels]
lgd = g.fig.legend(handles, labels, loc='upper center', ncol=5, bbox_to_anchor=(0.5, 1.05))
g.axes[0, 1].get_legend().remove()

plt.savefig("accuracy_excitations.png", dpi=600, bbox_extra_artists=(lgd, *g._margin_titles_texts,), bbox_inches="tight")
