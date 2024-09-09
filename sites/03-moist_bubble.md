Next: [How to analyse output data](04-plotting.md), Previous: [Setting up the environment](02-setup_environment.md), Up: [Main page](../README.md)

# How to prepare a simulation
In this workshop we simulate a rising moist bubble. The liquid-water buoyancy $b_l$ and the specific humidity $q$
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

![Cross section of the liquid water buoyancy (left panel) and specific humidity (centre panel). The right panel shows the basic-state stratification profile.[^1]](../figures/qj3319-fig-0002-m.jpg)

Above figure is taken from [Dritschel et al (2018)](https://doi.org/10.1002/qj.3319).

[^1]: Dritschel D G, Böing S J, Parker D J, Blyth A M. The moist parcel-in-cell method for modelling moist convection. Q J R Meteorol Soc. 2018; 144:1695–1718. https://doi.org/10.1002/qj.3319.

For further information about the example, read section 3.4 in [Frey et al (2023)](https://doi.org/10.1016/j.jcpx.2023.100136).

We provide you with a Python script that creates the gridded input fields. After following the instructions on
[how to load the Python virtual environment](02-setup_environment.md#how-to-load-the-python-virtual-environment),
you can run the script [input/write_moist_setup.py](../input/write_moist_setup.py) using the following command:

```bash
python write_moist_setup.py
```

which creates a file called `moist_<nx>x<ny>x<nz>.nc`, where `<nx>`, `<ny>` and `<nz>` are replaced by the number of grid cells per dimension (default: `nx = ny = nz = 64`).
You can call the script with the `--help` argument to get further information.



# How to run a simulation

The basic command to run a three-dimensional EPIC simulation is

```
epic3d --config <file.config>
```

where `<file.config>` is a placeholder for a configuration file that specifies all simulation parameters.
The configuration file for the moist bubble test case is already given in [input/moist.config](../input/moist.config).

The argument `field_file` which is currently set to `'moist_64x64x64.nc'` points to a netCDF file
which contains the initial gridded input data as well as domain specifications and physical quantities.

Cirrus uses the SLURM job scheduling system. To run a simulation please use the provided [batch script](../input/submit-job.sh).
A job is submitted with

```bash
sbatch submit-job.sh
```

> [!IMPORTANT]
> Our resources for this workshop are limited, so we kindly ask users to only use a maximum of 1 computing node per job.
> In addition, jobs should not run longer than 20 minutes.

> [!TIP]
> You can check the status of your submitted jobs with
> 
> ```bash
> squeue --me
> ```
> 
> A submitted or running job with id `<jobid>`  is cancelled calling
> 
> ```bash
> scancel <jobid>
> ```

Next: [How to analyse output data](04-plotting.md), Previous: [Setting up the environment](02-setup_environment.md), Up: [Main page](../README.md)
