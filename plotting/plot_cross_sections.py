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

    direction = ['x', 'y', 'z']
    planes = ['yz', 'xz', 'xy']
    parser.add_argument(
        '--plane',
        type=str,
        choices=planes,
        default='xz',
        help='orientation')

    parser.add_argument(
        '--loc',
        type=int,
        help='grid point location where to do cross section')

    parser.add_argument(
        '--cmap',
        default=cc.cm['coolwarm'],
        help="colour map")

    parser.add_argument(
        '--cmap-norm',
        type=str,
        choices=[None, 'centered', 'log', 'symlog'],
        default=None,
        help="colour map norm")


    args = parser.parse_args()

    fname = args.filename
    steps = args.steps
    dset = args.dataset
    plane = args.plane
    loc = args.loc
    cmap = args.cmap
    cmap_norm = args.cmap_norm

    ncr = nc_reader()
    ncr.open(fname)

    origin = ncr.get_box_origin()
    extent = ncr.get_box_extent()
    ncells = ncr.get_box_ncells()
    dx = extent / ncells

    i = planes.index(plane)
    ng = ncells[i]

    if loc is None:
        loc = int(ncells[i] / 2)

    if (loc < 0) or (loc > ng):
        raise ValueError("Location outside bounds.")

    loc_label = direction[i] + ' = ' + str(round(origin[i] + dx[i] * loc, 1)) + ' m'

    t = ncr.get_all('t')

    fig = plt.figure(figsize=(12, 8), dpi=200)
    grid = ImageGrid(fig, 111,
                     nrows_ncols=(2, 3),
                     aspect=True,
                     axes_pad=(0.38, 0.35),
                     direction='row',
                     share_all=True,
                     cbar_location="right",
                     cbar_mode='single',
                     cbar_size="4%",
                     cbar_pad=0.05)

    vmax = -10000
    vmin =  10000
    for i, step in enumerate(steps):
        data = ncr.get_dataset(step, name=dset)

        vmin = min(vmin, data.min())
        vmax = max(vmax, data.max())

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

        if not (i == 0 or i == 3):
            remove_yticks(ax)

        add_timestamp(ax, t[step], xy=(0.03, 1.04), fmt="%.2f")

        if not cbar is None:
            cbar.set_label(ncr.get_label(dset))

    add_annotation(grid[2], loc_label, xy=(0.7, 1.15))


    plt.savefig(plane + '-cross_section_location_' + str(loc) + '_' + dset + '.png',
                dpi=200, bbox_inches='tight')
    plt.close()

    ncr.close()

except Exception as ex:
    print(ex)
