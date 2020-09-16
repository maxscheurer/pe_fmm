import matplotlib
import seaborn as sns

def setup_mpl():
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
        "lines.linewidth": 1.5,
    }
    sns.set_context("paper")
    sns.set_palette("Set2")
    matplotlib.rcParams.update(pgf_with_rc_fonts)