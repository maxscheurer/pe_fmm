#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
import pandas as pd
import seaborn as sns

from common_plot import setup_mpl

# setup plot stuff
setup_mpl()

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

# create figure
fig, axes = plt.subplots(3, 2, figsize=(6, 8))
axes[0,0].set_axis_off()
axes[1,0].set_axis_off()
axes[2,0].set_axis_off()

df_pelib_single = df_pelib[df_pelib.nodes == 1]
sns.lineplot(ax=axes[1, 1], data=df_pelib_single, x="sites", y="time", hue="displaykey", err_style=None, marker=".", legend=None)

df_pelib_mpi = df_pelib[df_pelib.nodes == 10]
sns.lineplot(ax=axes[2, 1], data=df_pelib_mpi, x="sites", y="time", hue="displaykey", err_style=None, marker=".", legend=None)


inset = inset_axes(axes[1, 1], width=0.7, height=0.7, loc=2, borderpad=2.5)
sns.lineplot(ax=inset, data=df_pelib_single, x="sites", y="time", hue="displaykey", err_style=None, marker=".",
             legend=None)
inset.set_xlabel("")
inset.set_ylabel("")
inset.set_ylim(0, 3)


inset = inset_axes(axes[2, 1], width=0.7, height=0.7, loc=2, borderpad=2.5)
sns.lineplot(ax=inset, data=df_pelib_mpi, x="sites", y="time", hue="displaykey", err_style=None, marker=".",
             legend=None)
inset.set_xlabel("")
inset.set_ylabel("")
inset.set_ylim(0, 0.3)


dfs = []
shells = np.arange(10, 35, 5, dtype=int)
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
df_cppe['displaykey'] = df_cppe.apply(lambda x: f"{x.jobtype.upper()} ({x.impl.upper()})", axis=1) 
df_cppe["time"] /= 3600

sns.lineplot(ax=axes[0, 1], data=df_cppe, x="nsites", y="time", hue="displaykey", err_style=None, marker=".", legend=None)

inset = inset_axes(axes[0, 1], width=0.7, height=0.7, loc=2, borderpad=2.5)
sns.lineplot(ax=inset, data=df_cppe, x="nsites", y="time", hue="displaykey", err_style=None, marker=".",
             legend=None)
inset.set_xlabel("")
inset.set_ylabel("")
inset.set_ylim(0, 3)

axes[0, 1].set_ylim([0,30])
axes[1, 1].set_ylim([0,30])
axes[2, 1].set_ylim([0, 5])
axes[0, 1].set_xlim([0,2e5])
axes[1, 1].set_xlim([0,2e5])
axes[2, 1].set_xlim([0,2e5])
axes[0, 1].set_yticks([0, 5, 10, 15, 20, 25])
axes[1, 1].set_yticks([0, 5, 10, 15, 20, 25])
axes[2, 1].set_yticks([0, 1, 2, 3, 4])
axes[0, 1].set_ylabel("Wall time (hours)")
axes[1, 1].set_ylabel("Wall time (hours)")
axes[2, 1].set_ylabel("Wall time (hours)")
axes[0, 1].set_xticks([])
axes[1, 1].set_xticks([])
axes[0, 1].set_xlabel('')
axes[1, 1].set_xlabel('')
axes[2, 1].set_xlabel('Number of particles')
axes[0,1].set_title('CPPE', pad=-12, y=1.001)
axes[1,1].set_title('PElib', pad=-12, y=1.001)
axes[2,1].set_title('PElib (10 nodes)', pad=-12, y=1.001)
plt.subplots_adjust(hspace=0.05)

plt.savefig('figure2.png', dpi=600)
plt.show()

