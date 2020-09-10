import os
import numpy as np
import cppe
from timings import Timer
import pandas as pd

def print_callback(string):
    print(string)

shell = 50

potfile = f"../potfiles/loprop_solvated_{shell}.pot"
potentials = cppe.PotfileReader(potfile).read()

timer = Timer()
options = {}
fmuls = cppe.MultipoleFields(potentials, options)
with timer.record("direct"):
    fs = fmuls.compute_tree()

data = {}
for ii, theta in enumerate([0.2, 0.3, 0.5, 0.7, 0.99]):
    for exp_order in [3,5,7]:
        options = {
    	    "summation_induced_fields": "fmm",
    	    "theta": theta,
    	    "tree_expansion_order": exp_order,
        }
        fmuls_tree = cppe.MultipoleFields(potentials, options) 
        with timer.record(f"tree_{theta}_{exp_order}"):
    	    fs_tree = fmuls_tree.compute_tree()
    
        fs = fs.reshape(len(potentials), 3)
        fs_tree = fs_tree.reshape(fs.shape)
        err_mu_i = np.linalg.norm(fs - fs_tree, axis=1) / np.linalg.norm(fs, axis=1)
        data[f"err_F_{theta}_{exp_order}"] = err_mu_i

df = pd.DataFrame(data=data)
df.to_csv(f"solvated_{shell}_errors.csv")
