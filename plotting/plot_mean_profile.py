#!/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from tools.nc_reader import nc_reader
import matplotlib as mpl
from tools.utils import *
from tools.mpl_style import *
import argparse
import os
from tools.mpl_beautify import *
import matplotlib as mpl

try:
    parser = argparse.ArgumentParser(
        description="Plot mean profile."
    )

    parser.add_argument(
        '--filename',
        type=str,
        help='field file path and file name')

    parser.add_argument(
        '--steps',
        type=int,
        nargs=6,
        required=True,
        help='which six steps?')

    parser.add_argument(
        '--dataset',
        type=str,
        required=True,
        help='which field to plot?')

    args = parser.parse_args()

    fname = args.filename
    steps = args.steps
    dset = args.dataset

    ncr = nc_reader()
    ncr.open(fname)

    t = ncr.get_all('t')
    z = ncr.get_all('z')


    fig, axs = plt.subplots(nrows=1, ncols=6, figsize=(16, 4), dpi=200, sharey=True)

    mpl.rcParams['lines.linewidth'] = 1.5
    mpl.rcParams['font.size'] = 14

    for j, step in enumerate(steps):

        data = ncr.get_dataset(step=step, name=dset, copy_periodic=False)

        prof = data.mean(axis=(0, 1))

        axs[j].plot(prof, z, color='blue')

        axs[j].grid(linestyle='dashed', zorder=-2)
        if j == 0:
            axs[j].set_ylabel(r'$z$')
        add_timestamp(axs[j], t[step], xy=(0.03, 1.06), fmt="%.1f")

        if j > 0:
            remove_yticks(axs[j])

    # 24 June 2024
    # https://stackoverflow.com/a/7066293
    fig.suptitle(r'Height profile of horizontal ' + ncr.get_label(dset) + ' mean', y=1.10)

    ncr.close()

    plt.savefig(dset + '_mean_profile.png', dpi=200, bbox_inches='tight')
    plt.close()

except Exception as ex:
    print(ex)

