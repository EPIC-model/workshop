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
x_file=ds_file['x_position'].values[0]
y_file=ds_file['y_position'].values[0]
z_file=ds_file['z_position'].values[0]

x0_min, x0_max = 2700, 3580
y0_min, y0_max = 2700, 3580
z0_min, z0_max = 3800, 4700

x_mask=(x_file>x0_min)&(x_file<x0_max)
y_mask=(y_file>y0_min)&(y_file<y0_max)
z_mask=(z_file>z0_min)&(z_file<z0_max)
tracked_mask= x_mask & y_mask & z_mask

x_current = ds_file['x_position'].values[0][tracked_mask]
y_current = ds_file['y_position'].values[0][tracked_mask]
z_current = ds_file['z_position'].values[0][tracked_mask]
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([0, 6280])
ax.set_ylim([0, 6280])
ax.set_zlim([0, 6280])
ax.scatter(x_current, y_current, z_current, s=1, color='green')
plt.savefig('bw_anim_'+str(file_index)+'.png')
plt.close()

bw_tracked_label=label_file
for bw_index in range(file_index - 1, -1, -1):
    ds_current=xr.open_dataset(parcel_files[bw_index])
    labels=ds_current['label'].values[0]
    x_current = ds_current['x_position'].values[0]
    y_current = ds_current['y_position'].values[0]
    z_current = ds_current['z_position'].values[0]
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([0, 6280])
    ax.set_ylim([0, 6280])
    ax.set_zlim([0, 6280])
    ax.scatter(x_current[bw_tracked_label-1][tracked_mask], y_current[bw_tracked_label-1][tracked_mask], z_current[bw_tracked_label-1][tracked_mask], s=1, color='green')
    plt.savefig('bw_anim_'+str(bw_index)+'.png')
    bw_tracked_label=labels[bw_tracked_label-1]
    plt.close()
