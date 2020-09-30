import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from scipy import constants

from common_plot import setup_mpl

# setup_mpl()

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
        dfa["exp_order"] = exp_order
        
        for e in errors:
            dfa[f"error_{e}"] = np.abs(dfa[e] - adc_direct[e])
        all_dfs.append(dfa)

df = pd.concat(all_dfs, ignore_index=True)

# df = pd.melt(df, id_vars=['excitation', 'theta', 'exp_order'], value_vars=["error_" + e for e in errors],
#                   value_name="error", var_name="property")

df["error_excitation_energy"] *= eV

sns.catplot(x="excitation", y="error_excitation_energy", hue="theta", kind="bar",
            col="exp_order", data=df, log=False)
# sns.catplot(x="excitation", y="error", hue="theta", kind="bar",
#             col="exp_order", row="property", data=df)

plt.tight_layout()
plt.savefig("adc_accuracy.png", dpi=600)
