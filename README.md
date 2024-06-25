# Welcome to the EPIC workshop in Trieste!

This repository serves as a tutorial to show you how to prepare, run and analyse a moist bubble 
simulation using the [Elliptical Parcel-In-Cell (EPIC)](https://doi.org/10.1016/j.jcpx.2023.100136) 
method. During the course of this workshop (July 8th 2024), we provide you temporary access to the 
Cirrus cluster, a Tier-2 system of the EPSRC. All information how to access Cirrus is provided below. 
If you would like to work on your own laptop, feel free to do so. However, we might not be able to 
help you in case you face any issues regarding code compilation (not necessarily EPIC!).


### Table of Contents
- [Prerequisites](#prerequisites)
  - [Accessing the Cirrus cluster](#accessing-the-cirrus-cluster)
  - [Obtaining all resources](#obtaining-all-resources)
- [How to load the EPIC environment](#how-to-load-the-epic-environment)
- [How to load the Python virtual environment](#how-to-load-the-python-virtual-environment)
- [Moist bubble test case](#moist-bubble-test-case)
  - [How to prepare a simulation](#how-to-prepare-a-simulation)
  - [How to run a simulation](#how-to-run-a-simulation)
  - [How to analyse output data](#how-to-analyse-output-data)


***

## Prerequisites
### Accessing the Cirrus cluster

#### Summary:
  * Create SSH key-pair
  * Create SAFE account
  * Accept invite to `d185`, you will need to add the public part of an SSH key-pair to the `d185` machine account in SAFE when accepting the invite
  * Create an MFA token for the `d185` machine account on SAFE
  * Login to cirrus using an ssh client with: `ssh -i /path/to/your-ssh-private-key your_username@login.cirrus.ac.uk`
  * Type your TOTP/MFA code, which only be asked once a day (unless your IP changes, then you'll be asked for another TOTP)

#### Detailed Instructions:

The steps below will also be sent to your email, with the invite to join the `d185` project.

To get an account on Cirrus, a Tier 2 national HPC service from the EPSRC in the UK,
first you'll need an account on SAFE, the Service Administration service ran by EPCC.

You can register for a SAFE account following the steps detailed in the 
[SAFE documentation](https://epcced.github.io/safe-docs/safe-for-users/#registering-logging-in-passwords),
please register using the same email address that the invite was sent to.

You will need to accept the invite to join `d185`, create an SSH key-pair -- 
[more instructions here](https://docs.cirrus.ac.uk/user-guide/connecting/#ssh-key-pairs) -- 
and add it to the `d185` machine account.

You will then need to setup an MFA (multi-factor authentication) method for time based one 
time passwords (TOTP) and link it to your machine account, 
[see instructions here](https://docs.cirrus.ac.uk/user-guide/connecting/#time-based-one-time-passcode-totp-code).

To login, use:

```bash
ssh -i /path/to/your/ssh/key user@login.cirrus.ac.uk

# for example, for the user "d185-rfga" using a linux system:
ssh -i ~/.ssh/id_rsa_cirrus d185-rfga@login.cirrus.ac.uk
```
> [!NOTE]
> More details on how to login can be found [in the Cirrus documentation](https://docs.cirrus.ac.uk/user-guide/connecting/#ssh-clients).

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


***

## Moist bubble test case
In this example, the liquid-water buoyancy $b_l$ and the specific humidity $q$ 
distribution inside the moist bubble are given by
```math
\begin{align}
    b_{l}(\vec{x}') &= b_{\circ}
                     \left(
                         1 + \frac{0.3 x'y' -0.4 x'z' + 0.5 y'z'}{R^2}
                     \right)
                     S(h) \\
    q(\vec{x}') &= q_n + (q_{\circ}-q_n)S(h)\,,
\end{align}
```
with edge-smoothing function
```math
S(h) =
\left\{
\begin{align}
1 &{}\qquad h \leq 0 \\
1 - 10 h^3 + 15 h^4 - 6 h^5 &{}\qquad 0 < h < 1 \\
0 &{}\qquad h \geq 1
\end{align}
\right.
```
and $h\equiv(\|\vec{x}'\|/R-f_s)/(1-f_s)$, we choose $f_s=0.8$ and bubble radius $R = 800$. 
For further information about the example, read section 3.4 in
[Frey et al (2023)](https://doi.org/10.1016/j.jcpx.2023.100136).

### How to prepare a simulation
The basic command to run a three-dimensional EPIC simulation is
```
epic3d --config <file.config>
```
where `<file.config>` is a placeholder for a configuration file that specifies all simulation parameters.
The configuration file for the moist bubble test case is already given in [input/moist.config](input/moist.config).

The argument `field_file` which is currently set to `'moist_64x64x64.nc'` points to a netCDF file
which contains the initial gridded input data as well as domain specifications and
physical quantities. In this course, we use Python scripts to generate such input files.
After following the instructions on
[how to load the Python virtual environment](#how-to-load-the-python-virtual-environment),
you can run the script
[input/write_moist_setup.py](input/write_moist_setup.py) which creates a file called
`moist_<nx>x<ny>x<nz>.nc`, where `<nx>`, `<ny>` and `<nz>` are replaced
by the number of grid cells per dimension (default: `nx = ny = nz = 64`). You can call the script
with the `--help` argument to get further information.

### How to run a simulation
> [!IMPORTANT]
> Our resources for this workshop are limited, so we kindly ask users to only use a
> maximum of 1 computing node per job. In addition, jobs should not run longer than 20 minutes.

Cirrus uses the SLURM job scheduling system. To run a simulation please use the provided
[batch script](input/submit-job.sh). A job is submitted with
```bash
sbatch submit-job.sh
```

> [!TIP]
> You can check the status of your submitted jobs with
> ```bash
> squeue -u $USER
> ```
> A submitted or running job with id `<jobid>`  is cancelled calling
> ```bash
> scancel <jobid>
> ```

### How to analyse output data
In the plotting directory we collected some Python scripts that allow you to analyse the data. 
In order to facilitate their execution, add their directory to the `$PATH` environment variable with
```bash
export PATH=$PATH:/work/d185/d185/$USER/workshop-trieste/plotting
```
The provided scripts are
| Plotting script | Description |
| :--- | :--- |
| plot_cross_sections.py        | Create cross section plot from gridded data. |
| plot_mean_profile.py          | Calculate the horizontal mean and plot as a height profile. |
| plot_scatter.py               | Plot two parcel quantities against each other. |
| plot_histogram.py             | Make a histogram plot using parcel data. Check the different options with `--help`.
| plot_interesected_ellipses.py | Create a cross section plot where all intersection ellipses are displayed.

##### Example:
When you run the moist bubble case with the default settings, you can create a parcel cross section plot with
```bash
plot_interesected_ellipses.py --filename moist_0000000005_parcels.nc \
                              --steps 0 1 2 3 4 5 \
                              --dataset buoyancy \
                              --plane xz
```
which gives you this plot.

![Cross sections showing the ellipses obained from the intersection of the ellipsoids with the xz-plane through the centre of the y-axis.](xz-interesected_ellipses_location_32_buoyancy.png
"Cross sections showing the ellipses obained from the intersection of the ellipsoids with the xz-plane through the centre of the y-axis.")

For example, you can simply call
```bash
plot_cross_section --help
```
on the command line.

> [!TIP]
> The command `ncdump` is useful to inspect a netCDF file, i.e.
> ```bash
> ncdump filename.nc | less
> ```
> where `filename.nc` is a netCDF file.
