#!/bin/bash

# Please do not change the following options:
#SBATCH --job-name=EPIC
#SBATCH --time=0:59:0
#SBATCH --nodes=4
#SBATCH --tasks-per-node=36
#SBATCH --exclusive
#SBATCH --cpus-per-task=1
#SBATCH --account=d185
#SBATCH --partition=standard
#SBATCH --qos=standard

# Load the EPIC environment:
module use /work/d185/d185/shared/modules
module load gcc/10.2.0
module load openmpi/4.1.6
module load hdf5-epic
module load netcdf-epic
module load epic

# Change to the submission directory:
cd $SLURM_SUBMIT_DIR

export OMP_NUM_THREADS=1

# Launch the parallel job:
srun --kill-on-bad-exit epic3d --config two_cps.config
