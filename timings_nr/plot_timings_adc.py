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

column_names = ['SCF', 'ADC', 'PTC']

data = [
    [1.1, 0.8978, 0.7022],
    [3.5, 0.9225, 1.4775],
    [10.6, 0.9103, 3.6897],
    [32.0, 0.9211, 10.3789],
]
index = [
    "1x1x1", "3x1x1", "3x3x1", "3x3x3"
]
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=False)
fig.set_size_inches((8, 4))

df = pandas.DataFrame(data, columns=column_names, index=index)

for col, c in enumerate(column_names):
    f1 = df[c].values[0]
    if c == "ADC":
        continue
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
    d = np.loadtxt(f"{system}.txt")
    assert d.shape[0] == 3
    sp = Spectrum(d[:, 2], d[:, 3])
    spb = sp.broaden_lines(width=0.124, xmin=2.0, xmax=4.5)
    p = sp.plot(style="discrete", color=colors[si])
    spb.plot(style="continuous", color=colors[si], label=system)
plt.xlabel("Energy [eV]")
plt.ylabel("Oscillator strength")
plt.xlim([2.0, 4.5])
plt.axhline(0.0, color='gray', lw=0.5)
plt.legend()
fig.suptitle("PE-ADC(2)")

plt.tight_layout()
plt.savefig("nilered_adc_timings_spectra.png", dpi=300)
plt.show()
