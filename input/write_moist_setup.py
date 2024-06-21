#!/usr/bin/env python
import numpy as np
from tools.nc_fields import nc_fields
import argparse

try:
    parser = argparse.ArgumentParser(
        description="Write parcels for moist setup."
    )

    parser.add_argument(
        "--ngrid",
        type=int,
        required=False,
        default=54,
        help="number of grid cells per dimension",
    )

    args = parser.parse_args()

    # should eventually read these from namelist?
    RH = 0.8
    z_c = 2500.0
    mu = 0.9
    z_d = 4000.0
    z_m = 5000.0
    r_plume = 800.0
    e_values = np.array([0.3, -0.4, 0.5])
    height_c = 1000.0
    q0 = 0.015
    theta_0 = 300.0
    ngrid = args.ngrid
    n_par_res = 2  # how many parcels per grid box in each dimension
    gravity = 10.0
    L_v = 2.5e6
    c_p = 1000.0
    r_smooth_frac=0.8

    l_lower_boundry_zeta_zero = 'true'
    l_upper_boundry_zeta_zero = 'true'

    # domain origin
    origin = np.array([0, 0, 0])

    # domain extent
    extent = np.array([6280., 6280., 6280.])

    # number of grid cells in each dimension
    nx = ngrid
    ny = ngrid
    nz = ngrid

    # generate data
    if RH > 1.0:
        print("Error: Relative humidity fraction must be < 1.")
        quit()

    h_pl = q0 * np.exp(-z_c / height_c)

    print("Humidity inside the plume is " + str(h_pl))

    if (mu > 1.0) or (mu <= RH):
        print("Error: mu must be between H and 1. The selected value is " + str(mu))
        quit()

    h_bg = mu * h_pl

    print("Background humidity is " + str(h_bg))

    z_b = height_c * np.log(q0 * RH / h_bg)

    print("Base of mixed layer is " + str(z_b))

    dbdz = (
        (gravity * L_v / (c_p * theta_0))
        * (h_pl - q0 * np.exp(-z_m / height_c))
        / (z_m - z_d)
    )

    print("The buoyancy frequency in the stratified zone is " + str(np.sqrt(dbdz)))

    # Also obtain the plume liquid-water buoyancy (using also z_b):
    b_pl = dbdz * (z_d - z_b)

    print("The plume liquid water buoyancy b_pl = " + str(b_pl))
    print("corresponding to (theta_l-theta_0)/theta_0 = " + str(b_pl * gravity))

    if 2.0 * r_plume > z_b:
        print("Error: Plume radius is too big. At most it can be " + str(0.5 * z_b))
        quit()

    radsq = r_plume ** 2
    e_values = e_values / radsq

    if origin[2] > 0.0:
        print("The vertical origin must be zero.")
        quit()

    print("Box layout:")
    print("z_max           =" + str(extent[2]))
    print("z_m             =" + str(z_m))
    print("z_d             =" + str(z_d))
    print("z_c             =" + str(z_c))
    print("z_b             =" + str(z_b))
    print("zmin            =" + str(origin[2]))
    print("top of plume    =" + str(2.0 * r_plume))
    print("bottom of plume =" + str(0.0))

    # domain centre
    centre = 0.5 * (2.0 * origin + extent)

    # mesh spacings
    dx = extent[0] / nx
    dy = extent[1] / ny
    dz = extent[2] / nz

    xi   = np.zeros((nz+1, ny, nx))
    eta  = np.zeros((nz+1, ny, nx))
    zeta = np.zeros((nz+1, ny, nx))

    hum = np.zeros((nz+1, ny, nx))
    buoy = np.zeros((nz+1, ny, nx))

    # ranges from 0 to nx-1
    for i in range(nx):
        for j in range(ny):
            # ranges from 0 to nz
            for k in range(nz+1):
                x = origin[0] + i * dx
                y = origin[1] + j * dy
                z = origin[2] + k * dz

                rx = x - centre[0]
                ry = y - centre[1]
                rz = z - r_plume
                r2 = rx ** 2 + ry ** 2 + rz ** 2

                if r2 <= radsq*r_smooth_frac*r_smooth_frac:
                    buoy[k, j, i] = b_pl * (
                        1.0
                        + e_values[0] * rx * ry
                        + e_values[1] * rx * rz
                        + e_values[2] * ry * rz
                    )

                    hum[k, j, i] = h_pl

                elif r2 <= radsq:
                    # relative position on smoothed edge of bubble
                    r_edge = (np.sqrt(r2)-r_plume*r_smooth_frac)/(r_plume*(1.0-r_smooth_frac))
                    # use fifth order smoothstep function on edge
                    buoy[k, j, i] = b_pl * (
                        1.0
                        + e_values[0] * rx * ry
                        + e_values[1] * rx * rz
                        + e_values[2] * ry * rz
                    ) * (1.0-(6.0*r_edge**5-15.0*r_edge**4+10.0*r_edge**3))
                    hum[k, j, i] = h_pl*(1.0+(mu-1.0)*(6.0*r_edge**5-15.0*r_edge**4+10.0*r_edge**3))
                else:
                    if z < z_b:
                        # Mixed layer
                        buoy[k, j, i] = 0.0
                        hum[k, j, i] = h_bg
                    else:
                        # Stratified layer
                        buoy[k, j, i] = dbdz * (z - z_b)
                        hum[k, j, i] = q0 * RH * np.exp(-z / height_c)



    ncf = nc_fields()

    ncf.open('moist_' + str(nx) + 'x' + str(ny) + 'x' + str(nz) + '.nc')

    # write all provided fields
    ncf.add_field('buoyancy', buoy, unit='m/s^2')

    ncf.add_field('humidity', hum, unit='1')

    ncf.add_field('x_vorticity', xi,   unit='1/s')
    ncf.add_field('y_vorticity', eta,  unit='1/s')
    ncf.add_field('z_vorticity', zeta, unit='1/s')

    # write physical constants
    ncf.add_physical_quantity('gravity', gravity)
    ncf.add_physical_quantity('latent_heat', L_v)
    ncf.add_physical_quantity('specific_heat', c_p)

    ncf.add_physical_quantity('saturation_specific_humidity_at_ground_level', q0)
    ncf.add_physical_quantity('temperature_at_sea_level', theta_0)
    ncf.add_physical_quantity('scale_height', height_c)

    ncf.add_parameter('l_lower_boundry_zeta_zero', l_lower_boundry_zeta_zero)
    ncf.add_parameter('l_upper_boundry_zeta_zero', l_upper_boundry_zeta_zero)

    ncf.add_box(origin, extent, [nx, ny, nz])

    ncf.close()

except Exception as ex:
    print(ex)
