#### Obtaining all resources

Before you start, you must clone this repository to your working directory on Cirrus.
You can do this by using the command:

```bash
cd /work/d185/d185/$USER
git clone https://github.com/EPIC-model/workshop-trieste.git
```


***

## How to load the EPIC environment
In order to simplify your task, we have pre-installed a working EPIC executable.
After logging into Cirrus, you can load the environment with the following commands:
```bash
module use /work/d185/d185/shared/modules
module load gcc/10.2.0
module load openmpi/4.1.6
module load hdf5-epic
module load netcdf-epic
module load epic
```
If you would like to test the installation of EPIC, you can try out this [build script](build-epic.sh).
For this purpose, you would not load the EPIC module (last command). If you want to try on your own
laptop, you may have noticed that EPIC requires a working gfortran compiler, MPI and a netCDF
(requires HDF5) installation. To inspect the netCDF output files while a simulation is running,
you can additionally load the ncview module with
```bash
module load ncview-epic
```
> [!NOTE]
> You must be logged in with the flag `-X` in order to run ncview.

***

## How to load the Python virtual environment
You can prepare the input to EPIC and analyse its output using our tools written in Python.
For this purpose, you first need to load the virtual environment by typing the subsequent commands:
```bash
module load python/3.9.13
CONDA_ROOT=/work/d185/d185/shared/condaenvs
export CONDARC=${CONDA_ROOT}/.condarc
eval "$(conda shell.bash hook)"
conda activate epic-venv
```
> [!NOTE]
> The first four steps must be performed every time you log into the system.
>
> You can restore the original prompt by running ```conda deactivate``` twice.

The directory ```tools``` contains Python scripts that enable you to generate input data
and analyse the output data. To use these scripts, you  must make the Python interpreter
aware of the modules by setting the environment variable
```bash
export PYTHONPATH=$PYTHONPATH:/work/d185/d185/$USER/workshop-trieste
```
