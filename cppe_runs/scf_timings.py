import os
import numpy as np
from pyscf import gto, solvent
import cppe
from timings import Timer
import pandas as pd
import sys


def print_callback(string):
    print(string)

def scf_with_peoptions(mol, pe_options): 
    mf = mol.RHF()
    mf = solvent.PE(mf, pe_options)
    mf.conv_tol = 1e-8
    mf.conv_tol_grad = 1e-5
    mf.verbose = 1
    mf.kernel()
    assert mf.converged
    return mf

shells = np.arange(int(sys.argv[1]), int(sys.argv[2]), 5, dtype=int)
print(shells)
folder_xyz = "../../fmm_benchmarks/"
folder_pot = "../potfiles/"

columns = [
    "run", "n_sites", "theta", "exp_order", "ediff", "direct", "fmm"
]

ret = []
basis = "6-31+G*"
n_repeat = 3
print(f"Repeating SCF {n_repeat} times with basis {basis} using {os.environ['OMP_NUM_THREADS']} threads.")
for shell in shells:
    ret_shell = []
    for n in range(n_repeat):
        theta = 0.5
        exp_order = 5
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
        print(options)
        timer = Timer()
        
        options['summation_induced_fields'] = "direct"
        with timer.record("direct"):
            scfres_direct  = scf_with_peoptions(mol, options)
        
        options['summation_induced_fields'] = "fmm"
        options['theta'] = theta
        options['tree_expansion_order'] = exp_order
        with timer.record("fmm"):
            scfres_fmm = scf_with_peoptions(mol, options)
        
        n_sites = len(scfres_fmm.with_solvent.cppe_state.potentials)

        ediff = float(np.abs(scfres_direct.e_tot - scfres_fmm.e_tot))
        res = [
            n, n_sites, theta, exp_order, ediff, timer.total("direct"), timer.total("fmm")
        ]
        ret_shell.append(res)
    dfs = pd.DataFrame(data=ret_shell, columns=columns)
    dfs.to_csv(f"scf_timings_{shell}.csv")
    ret.extend(ret_shell)

df = pd.DataFrame(data=ret, columns=columns)
df.to_csv("scf_timings_all.csv")

