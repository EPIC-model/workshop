Welcome to the EPIC workshop in Trieste!
========================================

This repository serves as a tutorial in order to run and analyse a moist bubble simulation using the [Elliptical Parcel-in-Cell method](https://doi.org/10.1016/j.jcpx.2023.100136). We provide you temporary access to the Cirrus cluster, a Tier-2 system of the EPSRC. All information how to access Cirrus is provided [here](system_access.md).

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
