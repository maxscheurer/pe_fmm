#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
import pandas

df_pelib = pandas.read_csv('pelib_data/fmm_timings.csv')


fig, axes = plt.subplots(2,2, figsize=(6,5))

# pelib SCF
axes[0, 1].plot(df_pelib['sites'], 1/3600*df_pelib['direct_t_scf'], '.-', label='SCF')
axes[0, 1].plot(df_pelib['sites'], 1/3600*df_pelib['fmm_t_scf'], '.-', label='SCF (FMM)')

axes[0, 1].plot(df_pelib['sites'], 1/3600*df_pelib['direct_t_lr'], '.-', label='LR')
axes[0, 1].plot(df_pelib['sites'], 1/3600*df_pelib['fmm_t_lr'], '.-', label='LR (FMM)')

axes[1, 1].plot(df_pelib['sites'], 1/3600*df_pelib['direct_10nodes_t_scf'], '.-')
axes[1, 1].plot(df_pelib['sites'], 1/3600*df_pelib['fmm_10nodes_t_scf'], '.-')

axes[1, 1].plot(df_pelib['sites'], 1/3600*df_pelib['direct_10nodes_t_lr'], '.-')
axes[1, 1].plot(df_pelib['sites'], 1/3600*df_pelib['fmm_10nodes_t_lr'], '.-')

axes[1,0].set_axis_off()

axes[0,0].set_xlabel(r'$N_{\mathrm{sites}}$')
#axes[0,1].set_xlabel(r'$N_{\mathrm{sites}}$')
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
inset.plot(df_pelib['sites'], 1/3600*df_pelib['direct_t_scf'], '.-', label='SCF')
inset.plot(df_pelib['sites'], 1/3600*df_pelib['fmm_t_scf'], '.-', label='SCF (FMM)')
inset.plot(df_pelib['sites'], 1/3600*df_pelib['direct_t_lr'], '.-', label='LR')
inset.plot(df_pelib['sites'], 1/3600*df_pelib['fmm_t_lr'], '.-', label='LR (FMM)')
inset.set_ylim(0,4)
inset.set_xticks([])

inset = inset_axes(axes[1,1], width=0.7, height=0.7, loc=2, borderpad=2.5)
inset.plot(df_pelib['sites'], 1/3600*df_pelib['direct_10nodes_t_scf'], '.-')
inset.plot(df_pelib['sites'], 1/3600*df_pelib['fmm_10nodes_t_scf'], '.-')
inset.plot(df_pelib['sites'], 1/3600*df_pelib['direct_10nodes_t_lr'], '.-')
inset.plot(df_pelib['sites'], 1/3600*df_pelib['fmm_10nodes_t_lr'], '.-')
inset.set_ylim(0, 0.4)
inset.set_xticks([])

plt.savefig('scaling.png')
plt.show()

