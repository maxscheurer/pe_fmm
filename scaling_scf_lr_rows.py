#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
import pandas as pd
import seaborn as sns

from common_plot import setup_mpl

# setup plot stuff
setup_mpl(1.35)

sns.set_theme("paper", palette="colorblind", style="ticks", font_scale=1.35)
sns.set_palette("colorblind")

cc = sns.color_palette()
sns.set_palette([cc[0], cc[1], cc[4], cc[2]])
cc = sns.color_palette()

df_pelib = pd.read_csv('pelib_data/fmm_timings.csv')
cols = df_pelib.columns.values.tolist()
cols.pop(0)
df_pelib = pd.melt(df_pelib, id_vars=['sites'], value_vars=cols,
                   value_name="time", var_name="run")
df_pelib['time'] /= 3600
df_pelib['impl'] = df_pelib['run'].apply(lambda x: (x.split('_'))[0])
df_pelib['nodes'] = df_pelib['run'].apply(lambda x: 10 if "10" in x else 1)
df_pelib['jobtype'] = df_pelib['run'].apply(lambda x: "scf" if "scf" in x else "lr")
df_pelib['displaykey'] = df_pelib.apply(lambda x: f"{x.jobtype.upper()} ({x.impl.upper()})", axis=1)
df_pelib['nsites'] = df_pelib['sites']


df_pelib_single = df_pelib[df_pelib.nodes == 1]
df_pelib_mpi = df_pelib[df_pelib.nodes == 10]

df_pelib_single['column'] = 'PElib/Dalton'
df_pelib_mpi['column'] = 'PElib/Dalton (10 nodes)'


dfs = []
shells = np.arange(10, 65, 5, dtype=int)
for shell in shells:
    df = pd.read_csv(f"cppe_runs/lr_timings_{shell}.csv")
    dfs.append(df)
df_cppe = pd.concat(dfs, ignore_index=True)
df_cppe["nsites"] = df_cppe["n_sites"]
df_orig = df_cppe.copy()
df_cppe = pd.melt(df_cppe, id_vars=['nsites', 'theta', 'exp_order'], value_vars=['direct_scf', 'fmm_scf', 'direct_lr', 'fmm_lr'],
                  value_name="time", var_name="runtype")
df_cppe['impl'] = df_cppe['runtype'].apply(lambda x: (x.split('_'))[0])
df_cppe['jobtype'] = df_cppe['runtype'].apply(lambda x: "scf" if "scf" in x else "lr")

implementation = {
    "fmm": "FMM",
    "direct": "Direct",
}

df_cppe['displaykey'] = df_cppe.apply(lambda x: f"{x.jobtype.upper()} ({implementation[x.impl]})", axis=1) 
df_cppe["time"] /= 3600
df_cppe["column"] = "CPPE/PySCF"

df = pd.concat([df_cppe, df_pelib_single, df_pelib_mpi], ignore_index=True)

# Plot the lines on two facets
g = sns.relplot(
    data=df,
    x="nsites", y="time",
    row="impl",
    hue="jobtype", col="column",
    kind="line",
    markers="o-",
    facet_kws=dict(sharey=False, sharex=False),
)
g.set_titles("{col_name}")
xlab = r"$N_\mathrm{sites}$"
wtl = "Wall time (hours)"
g.set_axis_labels(xlab, wtl)
plt.show()