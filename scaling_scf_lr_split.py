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

# # create figure
fig, all_axes = plt.subplots(2, 3, figsize=(12, 2*3.75), sharey=False, sharex=False)

axes = all_axes[0]
axes_fmm = all_axes[1]

df_pelib_single = df_pelib[df_pelib.nodes == 1]
xx = np.unique(df_pelib_single['sites'].values)
y_scf_direct = df_pelib_single.query('run == "direct_t_scf"')['time'].values
y_lr_direct = df_pelib_single.query('run == "direct_t_lr"')['time'].values
y_scf_fmm = df_pelib_single.query('run == "fmm_t_scf"')['time'].values
y_lr_fmm = df_pelib_single.query('run == "fmm_t_lr"')['time'].values
axes[1].plot(xx, y_scf_direct, "o-", color=cc[0])
axes_fmm[1].plot(xx, y_scf_fmm, "o-", color=cc[2])
axes[1].plot(xx, y_lr_direct, "o-", color=cc[1])
axes_fmm[1].plot(xx, y_lr_fmm, "o-", color=cc[3])

df_pelib_mpi = df_pelib[df_pelib.nodes == 10]
xx = np.unique(df_pelib_mpi['sites'].values)
y_scf_direct = df_pelib_mpi.query('run == "direct_10nodes_t_scf"')['time'].values
y_lr_direct = df_pelib_mpi.query('run == "direct_10nodes_t_lr"')['time'].values
y_scf_fmm = df_pelib_mpi.query('run == "fmm_10nodes_t_scf"')['time'].values
y_lr_fmm = df_pelib_mpi.query('run == "fmm_10nodes_t_lr"')['time'].values
axes[2].plot(xx, y_scf_direct, "o-", color=cc[0])
axes_fmm[2].plot(xx, y_scf_fmm, "o-", color=cc[2])
axes[2].plot(xx, y_lr_direct, "o-", color=cc[1])
axes_fmm[2].plot(xx, y_lr_fmm, "o-", color=cc[3])


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

xx = np.unique(df_cppe['nsites'].values)
y_scf_direct = df_cppe.query('runtype == "direct_scf"')['time'].values
y_lr_direct = df_cppe.query('runtype == "direct_lr"')['time'].values
y_scf_fmm = df_cppe.query('runtype == "fmm_scf"')['time'].values
y_lr_fmm = df_cppe.query('runtype == "fmm_lr"')['time'].values

axes[0].plot(xx, y_scf_direct, "o-", color=cc[0], label="SCF (Direct)")
axes_fmm[0].plot(xx, y_scf_fmm, "o-", color=cc[2], label="SCF (FMM)")
axes[0].plot(xx, y_lr_direct, "o-", color=cc[1], label="LR (Direct)")
axes_fmm[0].plot(xx, y_lr_fmm, "o-", color=cc[3], label="LR (FMM)")

axes[0].legend()
axes_fmm[0].legend()


axes[0].sharey(axes[1])
axes_fmm[0].sharey(axes_fmm[1])

xlab = r"$N_\mathrm{sites}$"
wtl = "Wall time (hours)"
for al in all_axes:
    for ax in al:
        ax.set_xticks(np.arange(0, 2e5 + 1, 5*1e4))
        ax.set_xticks(np.arange(0, 2e5 + 1, 5*1e4))
        ax.set_xticks(np.arange(0, 2e5 + 1, 5*1e4))
        ax.set_xlabel(xlab)
        ax.set_ylabel(wtl)

axes[0].set_title('CPPE/PySCF', fontweight='bold', pad=15)
axes[1].set_title('PElib/Dalton', fontweight='bold', pad=15)
axes[2].set_title('PElib/Dalton (10 nodes)', fontweight='bold', pad=15)

handles, labels = axes[0].get_legend_handles_labels()
handles2, labels2 = axes_fmm[0].get_legend_handles_labels()

handles.extend(handles2)
labels.extend(labels2)

plt.subplots_adjust(hspace=0.0)
plt.tight_layout()

lgd = fig.legend(handles, labels, loc='upper center', ncol=4, bbox_to_anchor=(0.5, 1.04))
axes[0].get_legend().remove()
axes_fmm[0].get_legend().remove()

plt.savefig('scaling_scf_lr.png', dpi=600,
            bbox_extra_artists=(lgd, ),
            bbox_inches="tight")
