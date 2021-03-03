import os
import numpy as np
from pyscf import solvent, gto
import cppe
from timings import Timer
import pandas as pd
import adcc
import sys

assert "intel_build" in cppe.__file__

adcc.set_n_threads(24)

def print_callback(string):
    print(string)

def adc_with_peoptions(mol, pe_options):
    mf = mol.RHF()
    mf = solvent.PE(mf, pe_options)
    mf.conv_tol = 1e-8
    mf.conv_tol_grad = 1e-6
    mf.verbose = 4
    mf.kernel()
    assert mf.converged
    state = adcc.adc2(mf, n_singlets=5, conv_tol=1e-5)
    return state

shell = int(sys.argv[1])
basis = "6-31+G*"

folder_pot = "../potfiles"
folder_xyz = "../../fmm_benchmarks/"

xyzfile = os.path.join(folder_xyz, f"solvated_{shell}", "pna.xyz")
with open(xyzfile, "r") as f:
    xyz = f.readlines()[2:]
    xyz = "\n".join([x.strip() for x in xyz])
mol = gto.Mole(atom=xyz, basis=basis)
mol.max_memory = 40000
mol.build()
options = {
    "potfile": os.path.join(folder_pot, f"loprop_solvated_{shell}.pot"),
    "induced_thresh": 1e-8,
}
adc_direct = adc_with_peoptions(mol, options)
adc_direct.to_dataframe().to_csv(f"adc_direct_{shell}.csv")

print(f"Running with basis {basis}.")
for ii, theta in enumerate([0.2, 0.3, 0.5, 0.7, 0.99]):
    for exp_order in [3, 5, 7]:
        options.update({
    	    "summation_induced_fields": "fmm",
    	    "theta": theta,
    	    "tree_expansion_order": exp_order,
        })
        adc_fmm = adc_with_peoptions(mol, options)
        adc_fmm.to_dataframe().to_csv(f"adc_{shell}_{theta}_{exp_order}.csv")
