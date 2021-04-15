#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=150G
#SBATCH --time=12:00:00

source ~/miniconda3/bin/activate base
conda activate fmm

export OMP_NUM_THREADS=1

export PYTHONPATH=$PYTHONPATH:~/fmm/pyscf
export PYTHONPATH=$PYTHONPATH:~/fmm/cppe/build/stage/lib

module load compiler/intel/19.1.2

python -u $1 $2 $3

