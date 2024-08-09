# Note: this script has a slightly different syntax to the other ones 
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse
import glob
mpl.use('agg')

parser = argparse.ArgumentParser(
    description="Scatter plot. This script creates a scatter plot where " \
                "the x and y axes are the original and final parcel height."
)

parser.add_argument(
    '--file',
    type=str,
    help='filename at final time')


args = parser.parse_args()
glob_string=args.file[:-21]+'*'+'_parcels.nc'

# Set up arrays
ds_file=xr.open_dataset(args.file)
parcel_files=np.sort(glob.glob(glob_string))
print('parcel_files')
print(parcel_files)

file_index=np.argmax(args.file==parcel_files)

label_file=ds_file['label'].values[0]
vol_file=ds_file['volume'].values[0]/10000000 # Scale for plotting purposes

z0_min, z0_max = 0, 36

z_file = ds_file['z_position'].values[0]
z_mask=(z_file>z0_min)&(z_file<z0_max)
fw_tracked_mask= z_mask * (np.random.rand(len(z_mask))>0.5) #x_mask & y_mask & z_mask

mask_current = fw_tracked_mask
x_current = ds_file['x_position'].values[0][mask_current]
y_current = ds_file['y_position'].values[0][mask_current]
z_current = ds_file['z_position'].values[0][mask_current]
humid_current = ds_file['qv'].values[0][mask_current]
lw_current = ds_file['ql'].values[0][mask_current]
mask_dry = lw_current == 0
mask_moist = lw_current != 0
x_dry, y_dry, z_dry = x_current[mask_dry], y_current[mask_dry], z_current[mask_dry]
x_moist, y_moist, z_moist = x_current[mask_moist], y_current[mask_moist], z_current[mask_moist]
lw_moist = lw_current[mask_moist]
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(x_dry, y_dry, z_dry, s=0.1, c=z_dry, cmap='YlOrRd', vmin=0.0000, vmax=2000.0)
fig.colorbar(sc, ax=ax, label='Height',extend = 'max', shrink = 0.5, pad=0.05) 
sc = ax.scatter(x_moist, y_moist, z_moist, s=0.1, c=lw_moist, cmap='winter', vmin=0, vmax=0.001)
fig.colorbar(sc, ax=ax, label='Liquid Water Content',extend = 'max', shrink = 0.5, pad =0.1) 
ax.set_xlim([-3200, 3200])
ax.set_ylim([-3200, 3200])
ax.set_zlim([0, 3200])
ax.set_aspect('equal')
plt.savefig('fw_anim_'+str(file_index)+'.png')
plt.close()

for fw_index in range(file_index + 1, len(parcel_files)):
    ds_current=xr.open_dataset(parcel_files[fw_index])
    labels=ds_current['label'].values[0]
    mask_current = fw_tracked_mask[labels-1]
    x_current = ds_current['x_position'].values[0][mask_current]
    y_current = ds_current['y_position'].values[0][mask_current]
    z_current = ds_current['z_position'].values[0][mask_current]
    humid_current = ds_current['qv'].values[0][mask_current]
    lw_current = ds_current['ql'].values[0][mask_current]
    mask_dry = lw_current == 0
    mask_moist = lw_current != 0
    x_dry, y_dry, z_dry = x_current[mask_dry], y_current[mask_dry], z_current[mask_dry]
    x_moist, y_moist, z_moist = x_current[mask_moist], y_current[mask_moist], z_current[mask_moist]
    lw_moist = lw_current[mask_moist]
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x_dry, y_dry, z_dry, s=0.1, c=z_dry, cmap='YlOrRd', vmin=0.0000, vmax=2000.0)
    fig.colorbar(sc, ax=ax, label='Height',extend = 'max', shrink = 0.5, pad=0.05) 
    sc = ax.scatter(x_moist, y_moist, z_moist, s=0.1, c=lw_moist, cmap='winter', vmin=0, vmax=0.001)
    fig.colorbar(sc, ax=ax, label='Liquid Water Content',extend = 'max', shrink = 0.5, pad =0.1) 
    ax.set_xlim([-3200, 3200])
    ax.set_ylim([-3200, 3200])
    ax.set_zlim([0, 3200])
    ax.set_aspect('equal')
    fw_tracked_mask = mask_current
    plt.savefig('fw_anim_'+str(fw_index)+'.png')
    plt.close()
