from tools.nc_reader import nc_reader
import matplotlib.pyplot as plt

try:
    parser = argparse.ArgumentParser(
        description="Scatter plot. This script creates a scatter plot where " \
                    "the x and y axes are different parcel datasets."
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
        '--datasets',
        type=str,
        nargs=2,
        help='Takes 2 datasets')


    args = parser.parse_args()

    dsets = args.datasets

    if not os.path.exists(args.filename):
        raise IOError("File '" + args.filename + "' does not exist.")

    ncr = nc_reader()

    ncr.open(args.filename)




    x_dset = ncr.get_dataset(args.step-1, dsets[0])
    y_dset = ncr.get_dataset(args.step-1, dsets[1])

    plt.figure(figsize=(8, 8), dpi=200)

    plt.scatter(x_dset, y_dset, marker='o', c='blue')

    plt.show()

    plt.close()

    ncr.close()

except Exception as ex:
    print(ex)
