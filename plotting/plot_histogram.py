#!/bin/env python
from tools.nc_reader import nc_reader
from tools.mpl_beautify import add_timestamp, add_number_of_parcels
from tools.mpl_style import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import os

try:
    parser = argparse.ArgumentParser(
        description="Histogram plot. This script creates a histogram from parcel data."
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
        '--dataset',
        type=str,
        help='Parcel quantity')

    parser.add_argument(
        '--bins',
        type=int,
        default=100,
        help='number of bins')

    parser.add_argument(
        '--density',
        action='store_true',
        help='Plot a probability density')

    parser.add_argument(
        '--log',
        action='store_true',
        help='Set y-axis to log scale')

    parser.add_argument(
        '--cumulative',
        action='store_true',
        help='Make cumulative plot')


    args = parser.parse_args()

    dset  = args.dataset

    if not os.path.exists(args.filename):
        raise IOError("File '" + args.filename + "' does not exist.")

    ncr = nc_reader()

    ncr.open(args.filename)

    data = ncr.get_dataset(args.step-1, dset)

    mpl.use("agg", force=True)
    plt.figure(figsize=(6, 4), dpi=200)

    plt.hist(x=data,
             density=args.density,
             bins=args.bins,
             log=args.log,
             cumulative=args.cumulative,
             histtype='step')

    xlabel = ncr.get_label(dset)
    plt.xlabel(xlabel)

    ylabel = 'bin count'
    if args.density:
        ylabel = 'probability density'

    if args.cumulative:
        ylabel = 'cumulative distribution'
    
    plt.ylabel(ylabel)

    t = ncr.get_dataset(args.step-1, name='t')

    add_timestamp(plt, t, xy=(0.70, 1.05))

    num = ncr.get_num_parcels(args.step-1)
    add_number_of_parcels(plt, num, xy=(0.01, 1.05))

    plt.tight_layout()

    plt.savefig('hist_plot_' + dset + '.png',
                bbox_inches='tight',
                dpi=400)

    plt.close()

    ncr.close()

except Exception as ex:
    print(ex)
