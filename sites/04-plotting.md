Previous: [Prepare and run simulation](03-moist_bubble.md), Up: [Main page](../README.md)

# How to analyse output data
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

# Plotting with provided scripts
In the [plotting](../plotting) directory we collected the following Python scripts:
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
which gives you this plot:

![Cross sections showing the ellipses obained from the intersection of the ellipsoids with the xz-plane through the centre of the y-axis.](../figures/xz-intersected_ellipses_location_32_buoyancy.png
"Cross sections showing the ellipses obained from the intersection of the ellipsoids with the xz-plane through the centre of the y-axis.")

You can open the image with:

```bash
display <plane>-intersected_ellipses_<loc>_<dataset>.png
# for example, the image above is
display xy-intersected_ellipses_32_buoyamcy.png
```

# Plotting with xarray

Alternatively, you can use the package [xarray](https://docs.xarray.dev/en/stable/user-guide/io.html) to visualize the data.
>
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

You can open the image with:

```bash
display xz-buoyancy-cross_section.png
```

![Cross sections through the centre of the y-axis.](../figures/xz-buoyancy-cross_section.png
"Cross sections through the centre of the y-axis.")
