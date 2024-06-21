# Welcome to the EPIC workshop in Trieste!

This repository serves as a tutorial to show you how to prepare, run and analyse a moist bubble simulation using the [Elliptical Parcel-In-Cell (EPIC)](https://doi.org/10.1016/j.jcpx.2023.100136) method. During the course of this workshop (July 8th 2024), we provide you temporary access to the Cirrus cluster, a Tier-2 system of the EPSRC. All information how to access Cirrus is provided below. If you would like to work on your own laptop, feel free to do so. However, we might not be able to help you in case you face any issues regarding code compilation (not necessarily EPIC!).


### Table of Contents
- [Prerequisites](#prerequisites)
  - [Accessing the Cirrus cluster](#accessing-the-cirrus-cluster)
  - [Obtaining all resources](#obtaining-all-resources)
- [How to load the EPIC environment](#how-to-load-the-epic-environment)
- [How to load the Python virtual environment](#how-to-load-the-python-virtual-environment)
- [Moist bubble test case](#moist-bubble-test-case)
  - [Prepare input](#prepare-input)
  - [Run simulation](#run-simulation)
  - [Analyse output](#analyse-output)


***
## Prerequisites
#### Accessing the Cirrus cluster
For further details please visit https://docs.cirrus.ac.uk/user-guide/connecting/.

#### Obtaining all resources
Before you start, you must clone this repository to your working directory on Cirrus. You can do this by
```bash
cd /work/d185/d185/$USER
git clone https://github.com/EPIC-model/workshop-trieste.git
```


***
## How to load the EPIC environment
In order to simplify your task, we have pre-installed a working EPIC executable. After logging into Cirrus, you can load the environment with the following commands:
```bash
module use /work/d185/d185/shared/modules
module load gcc/10.2.0
module load openmpi/4.1.6
module load hdf5-epic
module load netcdf-epic
module load epic
```
If you would like to test the installation of EPIC, you can try out this [build script](build-epic.sh). For this purpose, you would not load the EPIC module (last command). If you want to try on your own laptop, you may have noticed that EPIC requires a working gfortran compiler, MPI and a netCDF (requires HDF5) installation. To inspect the netCDF output files while the simulatio is running, you can additionally load the ncview module with
```bash
module load ncview-epic
```


***
## How to load the Python virtual environment
You can prepare the input to EPIC and analyse its output using our tools written in Python. For this purpose, you first need to load the virtual environment by typing the subsequent commands:
```bash
module load python/3.9.13
CONDA_ROOT=/work/d185/d185/shared/condaenvs
export CONDARC=${CONDA_ROOT}/.condarc
eval "$(conda shell.bash hook)"
conda activate epic-venv
```
Note that the first four steps must be performed every time you log into the system. You can restore the original prompt by running ```conda deactivate``` twice.

In the directory ```tools``` of this repository, we provide you with Python scripts that enable you to generate input data and analyse the output data. To use these scripts, you must make the Python interpreter aware of the modules by setting the
environment variable
```bash
export PYTHONPATH=$PYTHONPATH:/work/d185/d185/$USER/workshop-trieste
```


***
## Moist bubble test case

### Prepare input
A base EPIC configuration file is given in [input/moist.config](input/moist.config). The input data is provided by the `field_file` argument.

### Run simulation
Cirrus uses the SLURM job scheduling sytem. To run the simulation please use the provided [batch script](input/submit-job.sh). A job is submitted with
```bash
sbatch submit-job.sh
```
You can check the status of your submitted jobs with
```bash
squeue -u $USER
```

### Analyse output
EPIC generates a bunch of output files. Here, we focus on the Eulerian and Lagrangian diagnostic files.
