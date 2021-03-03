import pandas
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import numpy as np
from adcc.visualisation.Spectrum import Spectrum

def setup_mpl(font_scale=1.3):
    # Setup matplotlib
    tex_premable = [
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{amsmath}",
    ]
    pgf_with_rc_fonts = {
        # "pgf.texsystem": "pdflatex",
        # "font.family": "serif",
        # "text.usetex": True,
        # "text.latex.preamble": tex_premable,
        # "pgf.rcfonts": False,
        # "pgf.preamble": tex_premable,
        "lines.linewidth": 1.5,
    }
    sns.set_context("paper", font_scale=font_scale)
    sns.set_palette("colorblind")
    matplotlib.rcParams.update(pgf_with_rc_fonts)

setup_mpl()

column_names = ['SCF', 'LR']

data = [
    [8750.815,  5825.44],
    [24992.314,  16599.66],
    [74098.246,  49755.77],
    [215841.968, 144952.05],
]
index = [
    "1x1x1", "3x1x1", "3x3x1", "3x3x3"
]
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=False)
fig.set_size_inches((8, 4))

df = pandas.DataFrame(data, columns=column_names, index=index)

df /= 3600

for col, c in enumerate(column_names):
    f1 = df[c].values[0]
    for i in range(1, 4):
        val = df[c].values[i]
        factor = val/f1
        offset = np.sum(df.values[i, :col])
        print(offset, offset + val / 2.0)
        ax1.annotate(f"{factor:.1f}x",
                    xy=(i, offset + val / 2.0), xytext=(0, -6), ha='center', va='bottom',
                    textcoords="offset points", fontsize=10,
                    )

df.plot.bar(stacked=True, ax=ax1)

ax1.set_xlabel("System")
ax1.set_ylabel("Time [hours]")

colors = sns.color_palette("husl", 8)
for si, system in enumerate(index):
    d = np.loadtxt(f"tddft_{system}.txt", delimiter=',')
    # d = d[:3, :]
    # assert d.shape[0] == 3
    sp = Spectrum(d[:, 0], d[:, 1])
    spb = sp.broaden_lines(width=0.124, xmin=2.0, xmax=4.5)
    p = sp.plot(style="discrete", color=colors[si])
    spb.plot(style="continuous", color=colors[si], label=system)
plt.xlabel("Energy [eV]")
plt.ylabel("Oscillator strength")
plt.axhline(0.0, color='gray', lw=0.5)
plt.xlim([2.0, 4.5])
plt.legend()
fig.suptitle("PE-TDDFT")

plt.tight_layout()
plt.savefig("nilered_tddft_timings_spectra.png", dpi=300)
plt.show()
