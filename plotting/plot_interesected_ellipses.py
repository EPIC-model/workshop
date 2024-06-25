#!/bin/env python
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
import matplotlib.colors as cls

try:
    parser = argparse.ArgumentParser(
        description="Plot all ellipses that are obtained from the intersection of a " \
                    "plane (either 'xy', 'xz' or 'yz') with the ellipsoids.")
    )

    parser.add_argument(
        '--filename',
        type=str,
        help='parcel file path and file name')

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
        help='which quantity to plot?')

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

    args = parser.parse_args()

    fname = args.filename
    steps = args.steps
    dset = args.dataset
    plane = args.plane
    loc = args.loc
    cmap = args.cmap

    ncr = nc_reader()
    ncr.open(fname)

    origin = ncr.get_box_origin()
    extent = ncr.get_box_extent()
    ncells = ncr.get_box_ncells()
    dx = extent / ncells

    j = planes.index(plane)
    ng = ncells[j]

    if loc is None:
        loc = int(ncells[j] / 2)

    if (loc < 0) or (loc > ng):
        raise ValueError("Location outside bounds.")

    loc_label = direction[j] + ' = ' + str(round(origin[j] + dx[j] * loc, 1)) + ' m'
    xlabel = planes[j][0]
    ylabel = planes[j][1]

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

    origin = ncr.get_box_origin()
    extent = ncr.get_box_extent()

    for i, step in enumerate(steps):

        ax = grid[i]
        
        ell, indices = ncr.get_intersection_ellipses(step, plane, loc)
        data = ncr.get_dataset(step, name=dset)
        ax.add_collection(ell)
        ell.set_offset_transform(ax.transData)
        ell.set_clip_box(ax.bbox)
        ell.set_alpha(1.0)
        ell.set_rasterized(True)
        # 25 June 2024
        # https://matplotlib.org/stable/gallery/shapes_and_collections/ellipse_collection.html
        ell.set_array(data[indices].ravel())
        ell.set_cmap(cmap)
        ell.set_clim(vmin=vmin, vmax=vmax)

        ax.set_xlim([origin[0], origin[0]+extent[0]])
        ax.set_ylim([origin[1], origin[1]+extent[1]])

        if i < 3:
            remove_xticks(ax)
        else:
            ax.set_xlabel(xlabel)

        if not (i == 0 or i == 3):
            remove_yticks(ax)
        else:
            ax.set_ylabel(ylabel)

        if i == 0:
            cbar = ax.cax.colorbar(ell)
            cbar.set_label(ncr.get_label(dset))

        t = ncr.get_dataset(step, 't')
        add_timestamp(ax, t, xy=(0.03, 1.04), fmt="%.2f")

    add_annotation(grid[2], loc_label, xy=(0.7, 1.15))

    plt.savefig(plane + '-interesected_ellipses_location_' + str(loc) + '_' + dset + '.png',
                dpi=200, bbox_inches='tight')
    plt.close()

    ncr.close()

except Exception as ex:
    print(ex)
