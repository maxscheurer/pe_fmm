import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns
import matplotlib

colors = sns.color_palette("Set2")

def setup():
    # Setup matplotlib
    tex_premable = [
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{amsmath}",
    ]
    pgf_with_rc_fonts = {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "text.latex.preamble": tex_premable,
        "pgf.rcfonts": False,
        "pgf.preamble": tex_premable,
    }
    matplotlib.rcParams.update(pgf_with_rc_fonts)

setup()
sns.set_context("paper")

# TODO: add pelib results!!!
df_cppe = pd.read_csv("cppe_runs/solvated_50_errors.csv")

fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)
for ii, theta in enumerate([0.2, 0.3, 0.5, 0.7, 0.99]):
    for ax, exp_order in zip(axes, [3,5,7]):
        err_F_i = df_cppe[f"err_F_{theta}_{exp_order}"]
        sns.histplot(x=np.log10(err_F_i), ax=ax, stat="probability", label=fr"$\theta = {theta}$", color=colors[ii])
        ax.set_xlabel(r"$\log_{10} F^\mathrm{err}$")
        ax.set_xlim([-10, 0])
        ax.set_title(f"order = {exp_order}")
plt.legend()
plt.tight_layout()
plt.savefig("figure1.png", dpi=600)

