Welcome to the EPIC workshop in Trieste!
========================================

How to connect to the system
----------------------------
For further details please visit https://docs.cirrus.ac.uk/user-guide/connecting/.

How to load the EPIC environment
--------------------------------
After logging into Cirrus, we load the environment with the following commands:
```bash
module use /work/d185/d185/shared/modules
module load gcc/10.2.0
module load openmpi/4.1.6
module load hdf5-epic
module load netcdf-epic
module load epic
```

How to load the Python virtual environment
------------------------------------------
You can load the pre-installed virtual environment using the subsequent commands:
```bash
module load python/3.9.13
CONDA_ROOT=/work/d185/d185/shared/condaenvs
export CONDARC=${CONDA_ROOT}/.condarc
eval "$(conda shell.bash hook)"
conda activate epic-venv
```
Note that the first four steps must be performed every time you log into the system. You can restore the original prompt by running ```conda deactivate``` twice.
