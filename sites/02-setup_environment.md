Next: [Prepare and run simulation](03-moist_bubble.md), Previous: [Accessing the Cirrus cluster](01-cluster_access.md), Up: [Main page](../README.md)

# Setting up the environment
- [Obtaining all resources](#obtaining-all-resources)
- [How to load the EPIC environment](#how-to-load-the-epic-environment)
- [How to load the Python virtual environment](#how-to-load-the-python-virtual-environment)


## Obtaining all resources
Before you start, you must clone this repository to your working directory on Cirrus.
You can do this by using the command:

```bash
cd /work/tc066/tc066/$USER
git clone https://github.com/EPIC-model/workshop.git
```


***

## How to load the EPIC environment

In order to simplify your task, we have pre-installed a working EPIC executable.
After logging into Cirrus, you can load the environment with the following commands:

```bash
module use /work/tc066/tc066/shared/modules
module load epic
```

The `epic` module will automatically load all the other required modules (`gcc`, `mpi`, `hdf5`, and `netcdf`).
You can confirm which modules you have loaded with the `module list` command:

```bash
tc066-rfga@cirrus-login2:~$ module list
Currently Loaded Modulefiles:
 1) git/2.37.3   3) /mnt/lustre/e1000/home/y07/shared/cirrus-modulefiles/epcc/setup-env   5) gcc/10.2.0(default)      7) hdf5-epic     9) epic
 2) epcc/utils   4) htop/3.2.1                                                            6) openmpi/4.1.6(default)   8) netcdf-epic
```

If you would like to test the installation of EPIC, you can try out this [build script](../build-epic.sh).
For this purpose, you would not load the EPIC module (last command).
If you want to try on your own laptop, you may have noticed that EPIC requires a working gfortran compiler, MPI and a netCDF (requires HDF5) installation.
To inspect the netCDF output files while a simulation is running, you can additionally load the ncview module with

```bash
module load ncview-epic
```

To open an image file, load the ImageMagick module, and use the `display` command.

```bash
module load ImageMagick
```

> [!NOTE]
> Your ssh connection must have been made with the flag `-X` in order to run `ncview` or ImageMagick's `display`.

***

## How to load the Python virtual environment
You can prepare the input to EPIC and analyse its output using our tools written in Python.
For this purpose, you first need to load the virtual environment by typing the subsequent commands:

```bash
module load python/3.9.13
CONDA_ROOT=/work/tc066/tc066/shared/condaenvs
export CONDARC=${CONDA_ROOT}/.condarc
eval "$(conda shell.bash hook)"
conda activate epic-venv
```

> [!NOTE]
> The first five steps must be performed every time you log into the system.
>
> You can restore the original prompt by running ```conda deactivate``` twice.

The directory ```tools``` contains Python scripts that enable you to generate input data
and analyse the output data. To use these scripts, you  must make the Python interpreter
aware of the modules by setting the environment variable

```bash
export PYTHONPATH=$PYTHONPATH:/work/tc066/tc066/$USER/workshop
```

Next: [Prepare and run simulation](03-moist_bubble.md), Previous: [Accessing the Cirrus cluster](01-cluster_access.md), Up: [Main page](../README.md)
