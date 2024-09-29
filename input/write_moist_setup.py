#!/usr/bin/env python

"""
        Moist bubble setup based on

        Dritschel D G, Böing S J, Parker D J, Blyth A M.
        The moist parcel-in-cell method for modelling moist convection. Q J R Meteorol Soc. 2018; 144:1695–1718.
        https://doi.org/10.1002/qj.3319
"""

import numpy as np
from tools.nc_fields import nc_fields
import argparse

try:
    # -------------------------------------------------------------------------
    # Parser setup:

    parser = argparse.ArgumentParser(
        description="Generate gridded input data for the moist bubble setup.")

    parser.add_argument(
        "--ncells",
        type=int,
        default=64,
        help="Number of grid cells per dimension. Must be an even number")

    parser.add_argument(
        "--rth",
        type=float,
        default=800.0,
        help="Radius of spherical thermal [m]")

    parser.add_argument(
        "--zb",
        type=float,
        default = 2400.0,
        help="Height of mixed layer.")

    parser.add_argument(
        "--zc",
        type=float,
        default = 2500.0,
        help="Height of condensation [m]. Requirement: zc > zb.")

    parser.add_argument(
        "--zd",
        type=float,
        default=4000.0,
        help="Height of dry neutral buoyancy [m]. Requirement: zd > zc.")

    parser.add_argument(
        "--zm",
        type=float,
        default=5000.0,
        help="Height of moist neutral buoyancy [m]. Requirement: zm > zd.")

    parser.add_argument(
        "--q0",
        type=float,
        default=0.015,
        help="Saturation specific humidity at ground level.")

    parser.add_argument(
        "--theta0",
        type=float,
        default=300.0,
        help="Mean liquid water potential temperature.")

    parser.add_argument(
        "--g",
        type=float,
        default=10.0,
        help="Gravitational acceleration (default: 10)")

    parser.add_argument(
        "--Lv",
        type=float,
        default=2.5e6,
        help="Latent heat (default: 2.5e6)")

    parser.add_argument(
        "--cp",
        type=float,
        default=1000.0,
        help="Specific heat (default: 1000)")

    parser.add_argument(
        "--RH",
        type=float,
        default=0.8,
        help="Relative humidity of environment [-]")

    # -------------------------------------------------------------------------
    # Read parser arguments:

    args = parser.parse_args()

    # should eventually read these from namelist?
    RH = args.RH
    zc = args.zc
    zb = args.zb
    zd = args.zd
    zm = args.zm
    rth = args.rth
    height_c = 1000.0
    q0 = args.q0
    theta_0 = args.theta0
    ncells = args.ncells
    g = args.g
    Lv = args.Lv
    cp = args.cp

    print()
    print("Input parameters:")
    print("--------------------------------------------------------------------")
    print("Saturation specific humidity at ground level, q0: ", q0)
    print("Scaled latent heat, L/cp [K]:                     ", Lv / cp)
    print("Scale height:                                     ", height_c)
    print("Relative humidity:                                ", RH)
    print("Condensation level, zc:                           ", zc)
    print("Height of the top of the mixed layer, zb:         ", zb)
    print("Level of dry neutral stratification, zd:          ", zd)
    print("Level of moist neutral stratification, zm:        ", zm)
    print("Radius of spherical thermal, rth:                 ", rth)
    print()

    # -------------------------------------------------------------------------
    # Parameters not to be changed:

    r_smooth_frac=0.8

    # domain origin
    origin = np.array([0, 0, 0])

    # domain extent
    extent = np.array([6280., 6280., 6280.])

    # domain centre
    centre = 0.5 * (2.0 * origin + extent)

    # number of grid cells in each dimension
    nx = ncells
    ny = ncells
    nz = ncells

    # mesh spacings
    dx = extent[0] / nx
    dy = extent[1] / ny
    dz = extent[2] / nz

    # -------------------------------------------------------------------------
    # Initial input sanity checks:

    if ncells % 2 == 1:
        raise ValueError("Number of grid cells must be an even number!")


    rmin = np.sqrt(dx**2 + dy**2)
    if rth < rmin:
        raise ValueError("Plume radius (rp) too small! Requirement: rp >= " + str(round(rmin, 1)) + " meters")

    if g <= 0:
        raise ValueError("Gravity must be strictly positive.")

    if zd <= zc:
        raise ValueError("Height level of dry zone (zd) must be higher than height of condensation level (zc).")

    if zm <= zd:
        raise ValueError("Height level of moist zone (zm) must be higher than dry zone (zd).")


    # generate data
    if RH > 1.0:
        raise ValueError("Relative humidity fraction must be < 1.")


    # Specific humidity fraction inside thermal
    qth = q0 * np.exp(-zc / height_c)

    # Specific humidity fraction outside thermal
    mu = (q0 * RH) / (qth * np.exp(zb / height_c))
    
    qenv = mu * qth

    if (mu > 1.0):
        print("Warning: mu above 1 implies thermal drier than environment. The selected value is " + str(mu))

    if (mu <= RH):
        print("Warning: mu must be above RH to avoid saturation in mixed layer. The selected value is " + str(mu))

    # Latent buoyancy, equation 30
    bm = g * Lv * q0  / (cp * theta_0)

    # N^2, equation 32
    dbdz = (
        (g * Lv / (cp * theta_0))
        * (qth - q0 * np.exp(-zm / height_c))
        / (zm - zd)
    )

    # Thermal liquid water buoyancy, equation 32
    b_pl = dbdz * (zd - zb)

    if 2.0 * rth > zb:
        raise ValueError("Plume radius is too big. At most it can be " + str(0.5 * zb))

    radsq = rth**2
    e_values = np.array([0.3, -0.4, 0.5])
    e_values = e_values / radsq

    if origin[2] > 0.0:
        raise ValueError("The vertical origin must be zero.")

    print()
    print("Derived parameters:")
    print("--------------------------------------------------------------------")
    print("Specific humidity fraction inside thermal, qth:   ", qth)
    print("Specific humidity fraction outside thermal, qenv: ", qenv)
    print("Specific humdity ratio, mu = qenv / qth:          ", mu)
    print("Buoyancy frequency in the stratified zone, N:     ", np.sqrt(dbdz))
    print("Latent buoyancy:                                  ", bm)
    print("Thermal liquid water buoyancy:                    ", b_pl)
    #print("corresponding to (theta_l-theta_0)/theta_0 = " + str(b_pl * g))
    print()

    # -------------------------------------------------------------------------
    # Create input fields:

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
                rz = z - rth
                r2 = rx ** 2 + ry ** 2 + rz ** 2

                if r2 <= radsq*r_smooth_frac*r_smooth_frac:
                    buoy[k, j, i] = b_pl * (
                        1.0
                        + e_values[0] * rx * ry
                        + e_values[1] * rx * rz
                        + e_values[2] * ry * rz
                    )

                    hum[k, j, i] = qth

                elif r2 <= radsq:
                    # relative position on smoothed edge of bubble
                    r_edge = (np.sqrt(r2)-rth*r_smooth_frac)/(rth*(1.0-r_smooth_frac))
                    # use fifth order smoothstep function on edge
                    buoy[k, j, i] = b_pl * (
                        1.0
                        + e_values[0] * rx * ry
                        + e_values[1] * rx * rz
                        + e_values[2] * ry * rz
                    ) * (1.0-(6.0*r_edge**5-15.0*r_edge**4+10.0*r_edge**3))
                    hum[k, j, i] = qth*(1.0+(mu-1.0)*(6.0*r_edge**5-15.0*r_edge**4+10.0*r_edge**3))
                else:
                    if z < zb:
                        # Mixed layer
                        buoy[k, j, i] = 0.0
                        hum[k, j, i] = qenv
                    else:
                        # Stratified layer
                        buoy[k, j, i] = dbdz * (z - zb)
                        hum[k, j, i] = q0 * RH * np.exp(-z / height_c)



    # -------------------------------------------------------------------------
    # Write input data to file:

    ncf = nc_fields()

    ncf.open('moist_' + str(nx) + 'x' + str(ny) + 'x' + str(nz) + '.nc')

    # write all provided fields
    ncf.add_field('buoyancy', buoy, unit='m/s^2')

    ncf.add_field('humidity', hum, unit='1')

    ncf.add_field('x_vorticity', xi,   unit='1/s')
    ncf.add_field('y_vorticity', eta,  unit='1/s')
    ncf.add_field('z_vorticity', zeta, unit='1/s')

    # write physical constants
    ncf.add_physical_quantity('gravity', g)
    ncf.add_physical_quantity('latent_heat', Lv)
    ncf.add_physical_quantity('specific_heat', cp)

    ncf.add_physical_quantity('saturation_specific_humidity_at_ground_level', q0)
    ncf.add_physical_quantity('temperature_at_sea_level', theta_0)
    ncf.add_physical_quantity('scale_height', height_c)

    ncf.add_parameter('l_lower_boundry_zeta_zero', 'true')
    ncf.add_parameter('l_upper_boundry_zeta_zero', 'true')

    ncf.add_box(origin, extent, [nx, ny, nz])

    ncf.close()

except Exception as ex:
    print(ex)
