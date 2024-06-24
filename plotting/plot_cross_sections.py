import numpy as np
import matplotlib.pyplot as plt
from tools.nc_reader import nc_reader
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import ImageGrid
from tools.utils import *
from tools.mpl_style import *
import argparse
import os
from tools.mpl_beautify import *
import matplotlib as mpl
import colorcet as cc


try:
    parser = argparse.ArgumentParser(
        description="Plot field cross sections."
    )

    parser.add_argument(
        '--filename',
        type=str,
        help='parcel file path and file name')

    parser.add_argument(
        '--steps',
        type=int,
        nargs=6,
        help='which six steps?')

    parser.add_argument(
        '--dataset',
        type=str,
        nargs=1,
        help='which field to plot?')

    args = parser.parse_args()

    fname = args.filename
    steps = args.steps


    mpl.rcParams['font.size'] = 12


    plane = 'xz'
    loc = 64
    loc_label = r'$y = 0$'
    cmap = cc.cm['coolwarm']
    cmap_norm = None
    vmin = -1.0
    vmax = 1.0

    ncr = nc_reader()
    ncr.open(fname)

    t = ncr.get_all('t')

    fig = plt.figure(figsize=(8, 5), dpi=200)
    grid = ImageGrid(fig, 111,
                     nrows_ncols=(2, 3),
                     aspect=True,
                     axes_pad=(0.38, 0.3),
                     direction='row',
                     share_all=True,
                     cbar_location="right",
                     cbar_mode='single',
                     cbar_size="4%",
                     cbar_pad=0.05)

    for i, step in enumerate(steps):

        ax = grid[i]

        data = ncr.get_dataset(step, name=dset)

        im, cbar = make_imshow(ax=ax,
                               plane=plane,
                               loc=loc,
                               fdata=data,
                               step=step,
                               ncr=ncr,
                               cmap=cmap,
                               cmap_norm=cmap_norm,
                               vmin=vmin,
                               vmax=vmax,
                               colorbar=(i == 0), # this is fine because we explicity set vmin and vmax
                               cbar_ext=False)

        if i < 3:
            remove_xticks(ax)
        else:
            ax.set_xticks(ticks, ticklabs)

        if i == 0 or i == 3:
            ax.set_yticks(ticks, ticklabs)
        else:
            remove_yticks(ax)

        add_timestamp(ax, t[step], xy=(0.03, 1.06), fmt="%.2f")

        if not cbar is None:
            cbar.set_label(ncr.get_label(dset))

    add_annotation(grid[2], loc_label, xy=(0.8, 1.2))

    add_annotation(grid[0], labels[j], xy=(-0.3, 1.2))


    plt.savefig('cross_section' + '_' + dset + '.png', dpi=200, bbox_inches='tight')
    plt.close()

    ncr.close()

except Exception as ex:
    print(ex)
