#!/usr/bin/env python3
# Note: this script has a slightly different syntax to the other ones
import argparse
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

warnings.filterwarnings("ignore", module="pandas")

parser = argparse.ArgumentParser(
    description="Scatter plot. This script creates a scatter plot where "
    "the x and y axes are the original and final parcel height."
)

parser.add_argument("--start", type=str, help="filename at t=0")


parser.add_argument("--final", type=str, help="filename at end time")


parser.add_argument(
    "--colour", type=str, help="colour: corresponds to a variable at final time"
)

args = parser.parse_args()

# Set up arrays
ds_start = xr.open_dataset(args.start)
ds_end = xr.open_dataset(args.final)
z_start = ds_start["z_position"].values[0]
labels_start = ds_start["label"].values[0]

vol_end = ds_end["volume"].values[0] / 10000000  # Scale for plotting purposes
#  dil_end=ds_end['dilution'].values[0] #
hum_end = ds_end[args.colour].values[0]
z_end = ds_end["z_position"].values[0]
labels_end = ds_end["label"].values[0]

# Get the start order
start_order = np.argsort(labels_start)
ordered_z_start = z_start[start_order]

# Correct for indexing difference between fortran and python
mpl.use("agg", force=True)
plt.scatter(ordered_z_start[labels_end - 1], z_end, s=vol_end, c=hum_end)
plt.xlabel("z start")
plt.ylabel("z end")
my_title = "parcel " + args.colour
plt.title(my_title)
plt.colorbar()
plt.savefig("parcel_history.png")
