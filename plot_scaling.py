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
fig, axes = plt.subplots(2,2, sharey=False)

df_pelib_single = df_pelib[df_pelib.nodes == 1]
sns.lineplot(ax=axes[0, 1], data=df_pelib_single, x="sites", y="time", hue="displaykey", err_style=None, marker=".")

df_pelib_mpi = df_pelib[df_pelib.nodes == 10]
sns.lineplot(ax=axes[1, 1], data=df_pelib_mpi, x="sites", y="time", hue="displaykey", err_style=None, marker=".", legend=None)

axes[1,0].set_axis_off()
axes[0,0].set_xlabel(r'$N_{\mathrm{sites}}$')
axes[0,1].set_xlabel("")
axes[1,1].set_xlabel(r'$N_{\mathrm{sites}}$')

axes[0,0].set_ylabel('Wall time (hours)')
axes[0,1].set_ylabel('Wall time (hours)')
axes[1,1].set_ylabel('Wall time (hours)')

axes[0,1].set_xticks([])
axes[1,1].set_xticks(np.arange(0, 200001, 50000))
axes[0,0].set_xticks(np.arange(0, 200001, 50000))
plt.setp(axes[1,1].xaxis.get_majorticklabels(), rotation=45)
plt.setp(axes[0,0].xaxis.get_majorticklabels(), rotation=45)
plt.subplots_adjust(hspace=0.2, bottom=0.2, wspace=0.3)

axes[0,0].set_title('CPPE')
axes[0,1].set_title('PElib')
axes[1,1].set_title('PElib (10 nodes)')

axes[0,1].legend(loc=(-1.0,-1.1))

inset = inset_axes(axes[0,1], width=0.7, height=0.7, loc=2, borderpad=2.)
sns.lineplot(ax=inset, data=df_pelib_single, x="sites", y="time", hue="displaykey", err_style=None, marker=".",
             legend=None)
inset.set_xlabel("")
inset.set_ylabel("")
inset.set_ylim(0,4)
inset.set_xticks([])

inset = inset_axes(axes[1,1], width=0.7, height=0.7, loc=2, borderpad=2.5)
sns.lineplot(ax=inset, data=df_pelib_mpi, x="sites", y="time", hue="displaykey", err_style=None, marker=".",
             legend=None)
inset.set_xlabel("")
inset.set_ylabel("")
inset.set_ylim(0, 0.4)
inset.set_xticks([])

# CPPE results
dfs = []
shells = np.arange(10, 65, 5, dtype=int)
for shell in shells:
    df = pd.read_csv(f"cppe_runs/scf_timings_{shell}.csv")
    dfs.append(df)
df_cppe = pd.concat(dfs, ignore_index=True)
df_cppe["nsites"] = df_cppe["n_sites"]
df_orig = df_cppe.copy()
df_cppe = pd.melt(df_cppe, id_vars=['run', 'nsites', 'theta', 'exp_order'], value_vars=['direct', 'fmm'],
                  value_name="time", var_name="impl")
df_cppe["time"] /= 3600

sns.lineplot(ax=axes[0, 0], data=df_cppe, x="nsites", y="time", hue="impl", err_style=None, marker=".", legend=None)

inset = inset_axes(axes[0, 0], width=0.7, height=0.7, loc=2, borderpad=2.)
sns.lineplot(ax=inset, data=df_cppe, x="nsites", y="time", hue="impl", err_style=None, marker=".",
             legend=None)
inset.set_xlabel("")
inset.set_ylabel("")
inset.set_ylim(0,4)
inset.set_xticks([])

scf_ylim = [0, 30]
axes[0, 0].set_ylim(scf_ylim)
axes[0, 1].set_ylim(scf_ylim)

plt.savefig('figure2.png', dpi=600)
plt.show()

