# Moist bubble test case
 - [How to prepare a simulation](#how-to-prepare-a-simulation)
  - [How to run a simulation](#how-to-run-a-simulation)
  - [How to analyse output data](#how-to-analyse-output-data)
    - [Plotting with provided scripts](#plotting-with-provided-scripts)
    - [Plotting with xarray](#plotting-with-xarray)

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
Cirrus uses the SLURM job scheduling system. To run a simulation please use the provided
[batch script](input/submit-job.sh). A job is submitted with
```bash
sbatch submit-job.sh
```
> [!IMPORTANT]
> Our resources for this workshop are limited, so we kindly ask users to only use a
> maximum of 1 computing node per job. In addition, jobs should not run longer than 20 minutes.

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
EPIC writes the following files, where `<basename>` is to be replaced by the character
string that is passed to EPIC via the argument `output%basename` in the configuration file:

| Output file | Description  |
| :--- | :--- |
| `<basename>_xxxxxxxxxx_parcels.nc` | NetCDF containing parcel output where `xxxxxxxxxx` is replaced with the file number, e.g. `moist_0000000002_parcels.nc`. |
| `<basename>_fields.nc` | NetCDF file containing gridded field output. |
| `<basename>_field_stats.nc` | NetCDF file containing diagnostics evaluated on the Eulerian grid. |
| `<basename>_parcel_stats.nc` | NetCDF file containing diagnostics evaluated using the Lagrangian parcels. |
| `<basename>_alpha_time_step.asc` | ASCII file containing time step estimates for the maximum strain and maximum buoyancy gradient. |
| `<basename>.csv` | ASCII file containing timings of the individual components of the code. |

> [!NOTE]
> The frequency of writing to the respective netCDF files is controlled via the construct `output`
> in the configuration file.

> [!TIP]
> The command `ncdump` is useful to inspect a netCDF file, i.e.
> ```bash
> ncdump filename.nc | less
> ```
> where `filename.nc` is a netCDF file.

#### Plotting with provided scripts
In the [plotting](plotting) directory we collected the following Python scripts:
| Plotting script | Description |
| :--- | :--- |
| plot_cross_sections.py        | Create cross section plot from gridded data. |
| plot_mean_profile.py          | Calculate the horizontal mean and plot as a height profile. |
| plot_scatter.py               | Plot two parcel quantities against each other. |
| plot_histogram.py             | Make a histogram plot using parcel data. Check the different options with `--help`. |
| plot_intersected_ellipses.py  | Create a cross section plot where all intersection ellipses are displayed. |
| plot_parcel_history.py        | Create a scatter plot with the original and final parcel height. |

These scripts allow you to explore Eulerian and Lagrangian simulation data.
Information how to use these scripts is printed when running with the flag `--help`, e.g. `plot_cross_sections.py --help`.

> [!TIP]
> We suggest that you append the plotting directory to the `$PATH` environment variable with
> ```bash
> export PATH=$PATH:/work/tc066/tc066/$USER/workshop/plotting
> ```
> in order to facilitate the usage of the plotting scripts. After this operation you can, for example, simply
> type `plot_cross_sections.py --help` from any directory and without prefixing the Python interpreter.

For example, when you run the moist bubble case with the default settings, you can create a parcel cross section plot with
```bash
plot_intersected_ellipses.py --filename moist_0000000005_parcels.nc \
                              --steps 0 1 2 3 4 5 \
                              --dataset buoyancy \
                              --plane xz
```
which gives you this plot.

![Cross sections showing the ellipses obained from the intersection of the ellipsoids with the xz-plane through the centre of the y-axis.](figures/xz-intersected_ellipses_location_32_buoyancy.png
"Cross sections showing the ellipses obained from the intersection of the ellipsoids with the xz-plane through the centre of the y-axis.")

### Plotting with xarray
Alternatively, you can use the package [xarray](https://docs.xarray.dev/en/stable/user-guide/io.html) to visualize the data.
> [!NOTE]
> When loading the `pandas` package two warnings are thrown regarding the version of the packages `numexpr` and `bottleneck`. To suppress these warnings, you can use
> ```Python
> import warnings
> warnings.filterwarnings("ignore", module='pandas')
> ```
The following code snippet creates a cross section plot of the gridded buoyancy field.
```Python
import warnings
warnings.filterwarnings("ignore", module='pandas')

import matplotlib.pyplot as plt
import colorcet as cc
import xarray as xr


da = xr.open_dataset("moist_fields.nc")

buoy = da.buoyancy

# get a time series of xz-cross sections through the centre of the y-axis (grid point 32)
t_buoy2d = buoy.isel(t=slice(0, 24, 4), y=32)

g = t_buoy2d.plot(x="x", y="z", col="t", col_wrap=3, cmap=cc.cm['coolwarm'], figsize=(12, 7))

# fix the time format
times = da.t.dt.strftime("%H:%M:%S")
for i, ax in enumerate(g.axs.flat):
    ax.set_title("Time "+ times.data[i] + " (HH:MM:SS)")

plt.savefig('xz-buoyancy-cross_section.png', bbox_inches='tight', dpi=200)
plt.close()
```

![Cross sections through the centre of the y-axis.](figures/xz-buoyancy-cross_section.png
"Cross sections through the centre of the y-axis.")
