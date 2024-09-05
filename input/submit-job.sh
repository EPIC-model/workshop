#!/bin/bash

# Please do not change the following options:
#SBATCH --job-name=EPIC
#SBATCH --time=0:20:0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=36
#SBATCH --cpus-per-task=1
#SBATCH --account=tc066
#SBATCH --partition=standard
#SBATCH --qos=short

# Load the EPIC environment:
module use /work/tc066/tc066/shared/modules
module load epic

# Change to the submission directory:
cd $SLURM_SUBMIT_DIR

export OMP_NUM_THREADS=1

# Launch the parallel job:
srun --kill-on-bad-exit epic3d --config moist.config
