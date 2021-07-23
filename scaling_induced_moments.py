#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yaml
import statsmodels.api as sm

from common_plot import setup_mpl

# setup plot stuff
setup_mpl(1.35)

sns.set_theme("paper", palette="colorblind", style="ticks", font_scale=1.35)
sns.set_palette("colorblind")

# sites, induced, induced_fmm, #static, static_fmm
data = []
for s in range(10, 65, 5):
    df = pd.read_csv(f"cppe_runs/lr_timings_{s}.csv")
    nsites = df.n_sites.values[0]
    with open(f"cppe_runs/induced_solver/induced_moments_{s}.yml", "r") as ff:
        ret = yaml.safe_load(ff)
        data.append([nsites, ret['induced'], ret['induced_fmm']])
df = pd.DataFrame(data=data, columns=['nsites', 'induced_direct', 'induced_fmm'])
# df['ratio'] = df['induced_direct'] / df['induced_fmm']
df['lib'] = 'CPPE'

dfp = pd.read_csv("pelib_data/induced_solver_fmm.txt")
dfp2 = pd.read_csv("pelib_data/induced_solver_direct.txt")
dfp['induced_direct'] = dfp2['induced_direct']
dfp['iter_direct'] = dfp2['iter_direct']
dfp['lib'] = 'PElib'
print(dfp)

# get number of iterations
logfile = "cppe_runs/induced_solver/slurm-2268346.out"
with open(logfile, "r") as f:
    lines = f.readlines()
    lines = [l.strip() for l in lines]

counts_direct = []
counts_fmm = []
for ii, l in enumerate(lines):
    if "Solving direct summation" in l:
        for i in lines[ii + 1:]:
            if "Norm:" not in i:
                break
            else:
                count = i.split()[0]
        counts_direct.append(int(count) + 1)
    if "Solving FMM summation" in l:
        for i in lines[ii + 1:]:
            if "Norm:" not in i:
                break
            else:
                count_fmm = i.split()[0]
        counts_fmm.append(int(count_fmm) + 1)
df['iter_direct'] = counts_direct
df['iter_fmm'] = counts_fmm

df = pd.concat([df, dfp], ignore_index=True)

df['per_iter_fmm'] = df['induced_fmm'] / df['iter_fmm']
df['per_iter_direct'] = df['induced_direct'] / df['iter_direct']

# df = df.round(1)
print(df)

df.query('lib == "CPPE"').round(1).drop('lib', axis=1).to_latex('induced_cppe.tex', escape=True, index=False)
df.query('lib == "PElib"').round(1).drop('lib', axis=1).to_latex('induced_pelib.tex', escape=True, index=False)

piv = df.pivot(index="nsites", columns=["lib"], values=[
                                                        "induced_direct",
                                                        "iter_direct",
                                                        "per_iter_direct",
                                                        "induced_fmm",
                                                        "iter_fmm",
                                                        "per_iter_fmm"
                                                        ])
piv = piv.swaplevel(0, 1, axis=1).sort_index(axis=1)
print(piv.round(1))

exit(0)

xx = df['nsites'].values
# xx = sm.add_constant(xx)
# y_fmm = df['induced_fmm'].values
y_fmm = df['per_iter_fmm'].values
result = sm.OLS(y_fmm, xx).fit()

xc = np.arange(0, 2e5)
yc = result.params[0] * xc
# print(result.summary())


fig, ax = plt.subplots(nrows=1, ncols=1)
# ax.plot(df['nsites'], df['induced_direct'], "o-", label="Direct")
ax.plot(df['nsites'], df['per_iter_fmm'], "o-", label="FMM")
ax.plot(xc, yc, label="linear fit")

# ax.set_yscale('log')
# ax.set_xscale('log')
ax.set_xlabel(r"$N_\mathrm{sites}$")
ax.set_ylabel("Wall time (seconds)")
ax.legend()

# xx = np.log(df['nsites'].values)
# xx = sm.add_constant(xx)
# y_direct = np.log(df['induced_direct'].values)
# y_fmm = np.log(df['induced_fmm'].values)

# result = sm.OLS(y_direct, xx).fit()
# print(result.summary())

# result = sm.OLS(y_fmm, xx).fit()
# print(result.summary())

plt.tight_layout()
plt.show()