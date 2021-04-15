import os
import yaml
import sys

os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np
import cppe

from timings import Timer
import pandas as pd


shells = np.arange(int(sys.argv[1]), int(sys.argv[2]), 5, dtype=int)

for shell in shells:
    ret = {}
    print("Solving direct summation")
    timer = Timer()
    potfile = f"../../potfiles/loprop_solvated_{shell}.pot"
    potentials = cppe.PotfileReader(potfile).read()

    options = {}
    fmuls = cppe.MultipoleFields(potentials, options)
    indmom = cppe.InducedMoments(potentials, options)

    with timer.record("static"):
        fs = fmuls.compute()
    with timer.record("induced"):
        induced_moments = indmom.compute(fs, True)
    print(f"System {shell}")
    print(timer.describe())
    ret["shell"] = int(shell)
    ret["static"] = timer.total("static")
    ret["induced"] = timer.total("induced")
    
    timer = Timer()
    options = {
       "summation_induced_fields": "fmm",
       "theta": 0.5,
       "tree_expansion_order": 5,
    }
    print("Solving FMM summation")
    fmuls_tree = cppe.MultipoleFields(potentials, options) 
    indmom_tree = cppe.InducedMoments(potentials, options)
    with timer.record("static_fmm"):
        fs_tree = fmuls_tree.compute()
    with timer.record("induced_fmm"):
        induced_moments = indmom_tree.compute(fs_tree, True)
    ret["static_fmm"] = timer.total("static_fmm")
    ret["induced_fmm"] = timer.total("induced_fmm")
    with open(f"induced_moments_{shell}.yml", "w") as f:
        yaml.safe_dump(ret, f)
    print(timer.describe())
    print("------------------------")
