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

cc = sns.color_palette()
sns.set_palette([cc[0], cc[1], cc[4], cc[2]])

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
fig, axes = plt.subplots(1, 3, figsize=(12, 3.75), sharey=False)
print(axes)
# axes[0].set_axis_off()
# axes[1].set_axis_off()
# axes[2].set_axis_off()

df_pelib_single = df_pelib[df_pelib.nodes == 1]
sns.lineplot(ax=axes[1], data=df_pelib_single, x="sites", y="time", hue="displaykey", err_style=None, marker="o", legend=None, linewidth=2.0)

df_pelib_mpi = df_pelib[df_pelib.nodes == 10]
sns.lineplot(ax=axes[2], data=df_pelib_mpi, x="sites", y="time", hue="displaykey", err_style=None, marker="o", legend=None, linewidth=2.0)


inset = inset_axes(axes[1], width=1.0, height=1.0, loc=2, borderpad=2.8)
sns.lineplot(ax=inset, data=df_pelib_single, x="sites", y="time", hue="displaykey", err_style=None, marker="o",
             legend=None, linewidth=2.0)
inset.set_xlabel("")
inset.set_ylabel("")
inset.set_ylim(0, 3)
inset.set_xlim(0, 60000)


inset = inset_axes(axes[2], width=1.0, height=1.0, loc=2, borderpad=2.8)
sns.lineplot(ax=inset, data=df_pelib_mpi, x="sites", y="time", hue="displaykey", err_style=None, marker="o",
             legend=None, linewidth=2.0)
inset.set_xlabel("")
inset.set_ylabel("")
inset.set_ylim(0, 0.3)
inset.set_xlim(0, 60000)


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

sns.lineplot(ax=axes[0], data=df_cppe, x="nsites", y="time", hue="displaykey", err_style=None, marker="o", legend=True, linewidth=2.0)

inset = inset_axes(axes[0], width=1.0, height=1.0, loc=2, borderpad=2.8)
sns.lineplot(ax=inset, data=df_cppe, x="nsites", y="time", hue="displaykey", err_style=None, marker="o",
             legend=None, linewidth=2.0)
inset.set_xlabel("")
inset.set_ylabel("")
inset.set_ylim(0, 3)
inset.set_xlim(0, 60000)


axes[0].set_xlim([0,2e5])
axes[1].set_xlim([0,2e5])
axes[2].set_xlim([0,2e5])

axes[0].set_yticks(np.arange(0, 80, 10))
axes[1].set_yticks(np.arange(0, 80, 10))
axes[2].set_yticks([0, 1, 2, 3, 4])

axes[0].set_xticks(np.arange(0, 2e5 + 1, 5*1e4))
axes[1].set_xticks(np.arange(0, 2e5 + 1, 5*1e4))
axes[2].set_xticks(np.arange(0, 2e5 + 1, 5*1e4))

wtl = "Wall time (hours)"
axes[0].set_ylabel(wtl)
axes[1].set_ylabel(wtl)
axes[2].set_ylabel(wtl)

xlab = r"$N_\mathrm{sites}$"
axes[0].set_xlabel(xlab)
axes[1].set_xlabel(xlab)
axes[2].set_xlabel(xlab)
axes[0].set_title('CPPE/PySCF', pad=-12, y=1.001)
axes[1].set_title('PElib/Dalton', pad=-12, y=1.001)
axes[2].set_title('PElib/Dalton (10 nodes)', pad=-12, y=1.001)

handles, labels = axes[0].get_legend_handles_labels()
plt.subplots_adjust(hspace=0.0)
plt.tight_layout()

lgd = fig.legend(handles, labels, loc='upper center', ncol=4, bbox_to_anchor=(0.5, 1.09))
axes[0].get_legend().remove()

plt.savefig('scaling_scf_lr.png', dpi=600, bbox_extra_artists=(lgd,), bbox_inches="tight")


# cross-over points
def crossings(dfr, pt=1.0):
    nsites = np.unique(dfr['nsites'])
    for i in nsites:
        dscf = dfr.query(f"nsites == {i} and runtype == 'direct_scf'")['time'].values[0]
        fscf = dfr.query(f"nsites == {i} and runtype == 'fmm_scf'")['time'].values[0]

        dlr = dfr.query(f"nsites == {i} and runtype == 'direct_lr'")['time'].values[0]
        flr = dfr.query(f"nsites == {i} and runtype == 'fmm_lr'")['time'].values[0]
        # print(i, dscf, fscf)
        
        total_direct = dscf + dlr
        total_fmm = fscf + flr
        
        if pt*total_fmm < total_direct:
            print(f"cppe: Crossing point (factor {pt}) = {i}")
            return

def crossings_pelib(dfr, pt=1.0):
    nsites = np.unique(dfr['sites'])
    for i in nsites:
        dscf = dfr.query(f"sites == {i} and run == 'direct_t_scf'")['time'].values[0]
        fscf = dfr.query(f"sites == {i} and run == 'fmm_t_scf'")['time'].values[0]

        dlr = dfr.query(f"sites == {i} and run == 'direct_t_lr'")['time'].values[0]
        flr = dfr.query(f"sites == {i} and run == 'fmm_t_lr'")['time'].values[0]
        total_direct = dscf + dlr
        total_fmm = fscf + flr
        
        if pt*total_fmm < total_direct:
            print(f"pelib: Crossing point (factor {pt}) = {i}")
            return

for i in range(1, 11):
    crossings_pelib(df_pelib_single, i)
    crossings(df_cppe, i)