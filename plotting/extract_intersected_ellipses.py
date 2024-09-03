#!/bin/env python3
import argparse
import os

import numpy as np
from tools.nc_parcels import nc_parcels
from tools.nc_reader import nc_reader

try:
    parser = argparse.ArgumentParser(
        description="Extracts all ellipses that result from the intersection of "
        "ellipsoids with a plane. The plane can be either xz, xy or yz. The position "
        "'--loc' of the intersection point is specified in the form of grid points."
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
        '--plane',
        type=str,
        choices=['xy', 'xz', 'yz'],
        help='orientation of intersecting plane')

    parser.add_argument(
        '--loc',
        type=int,
        help='grid point of intersection')

    parser.add_argument(
        '--dataset',
        type=str,
        help='dataset to extract')

    args = parser.parse_args()

    if not os.path.exists(args.filename):
        raise IOError("File '" + args.filename + "' does not exist.")

    if not args.dataset:
        raise ValueError("Please select a parcel quantity with the option '--dataset'")

    ncr = nc_reader()

    ncr.open(args.filename)

    dset = ncr.get_dataset(args.step - 1, args.dataset)

    centres, B11, B12, V, ind = ncr.calculate_intersection_ellipses(args.step - 1, args.plane, args.loc)

    origin = ncr.get_box_origin()
    extent = ncr.get_box_extent()
    ncells = ncr.get_box_ncells()

    if args.plane == 'xy':
        origin = [origin[0], origin[1]]
        extent = [extent[0], extent[1]]
        ncells = [ncells[0], ncells[1]]
    elif args.plane == 'xz':
        origin = [origin[0], origin[2]]
        extent = [extent[0], extent[2]]
        ncells = [ncells[0], ncells[2]]
    elif args.plane == 'yz':
        origin = [origin[1], origin[2]]
        extent = [extent[1], extent[2]]
        ncells = [ncells[1], ncells[2]]

    ncr.close()

    ncp = nc_parcels()
    dirname = os.path.dirname(args.filename)
    basename = os.path.basename(args.filename)
    ncp.open(os.path.join(dirname, 'intersected_ellipses_step_' + str(args.step) + '_from_' + basename))
    ncp.add_box(origin, extent, ncells)

    ncp.add_dataset('x_position', centres[:, 0], unit='m')
    ncp.add_dataset('z_position', centres[:, 1], unit='m')
    ncp.add_dataset(args.dataset, dset[ind], units='1')

    ncp.add_dataset('volume', V, unit='m^2')
    ncp.add_dataset('B11', B11, unit='m^2')
    ncp.add_dataset('B12', B12, unit='m^2')

    ncp.close()

except Exception as ex:
    print(ex)
