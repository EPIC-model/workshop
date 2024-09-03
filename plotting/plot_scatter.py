#!/bin/env python3
import argparse
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from tools.mpl_beautify import add_number_of_parcels, add_timestamp
from tools.mpl_style import *
from tools.nc_reader import nc_reader

try:
    parser = argparse.ArgumentParser(
        description="Scatter plot. This script creates a scatter plot where "
                    "the x and y axes are different parcel datasets."
    )

    parser.add_argument(
        '--filename',
        type=str,
        help='parcel file path and file name')

    parser.add_argument(
        '--step',
        type=int,
        help='which step?')

    parser.add_argument(
        '--datasets',
        type=str,
        nargs=2,
        help='Takes 2 datasets')

    args = parser.parse_args()

    dsets = args.datasets

    if not os.path.exists(args.filename):
        raise IOError("File '" + args.filename + "' does not exist.")

    ncr = nc_reader()

    ncr.open(args.filename)

    x_dset = ncr.get_dataset(args.step - 1, dsets[0])
    y_dset = ncr.get_dataset(args.step - 1, dsets[1])

    mpl.use("agg", force=True)
    plt.figure(figsize=(7, 7), dpi=200)

    plt.scatter(x_dset, y_dset, marker='o', c='blue', s=2)

    xlabel = ncr.get_label(dsets[0]) + ' (' + ncr.get_units(dsets[0]) + ')'
    plt.xlabel(xlabel)

    ylabel = ncr.get_label(dsets[1]) + ' (' + ncr.get_units(dsets[1]) + ')'
    plt.ylabel(ylabel)

    t = ncr.get_dataset(args.step - 1, name='t')

    add_timestamp(plt, t, xy=(0.80, 1.02))

    num = ncr.get_num_parcels(args.step - 1)
    add_number_of_parcels(plt, num, xy=(0.01, 1.02))

    plt.tight_layout()

    plt.savefig('scatter_plot_' + dsets[0] + '_vs_' + dsets[1] + '.png',
                bbox_inches='tight',
                dpi=400)

    plt.close()

    ncr.close()

except Exception as ex:
    print(ex)
