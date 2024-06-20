from tools.nc_reader import nc_reader
from tools.mpl_beautify import *
from tools.mpl_style import *
from tools.units import *
import matplotlib.colors as cls
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import os


def _plot_parcels(ax, ncreader, step, coloring, vmin, vmax, draw_cbar=True, **kwargs):

    # 19 Feb 2021
    # https://stackoverflow.com/questions/43009724/how-can-i-convert-numbers-to-a-color-scale-in-matplotlib
    norm = cls.Normalize(vmin=vmin, vmax=vmax)
    cmap = kwargs.pop('cmap', plt.cm.viridis_r)

    origin = ncreader.get_box_origin()
    extent = ncreader.get_box_extent()
    ncells = ncreader.get_box_ncells()
    dx = extent / ncells

    timestamp = kwargs.pop('timestamp', True)
    nparcels = kwargs.pop('nparcels', True)
    timestamp_xy = kwargs.pop('timestamp_xy', (0.75, 1.05))
    timestamp_fmt = kwargs.pop('timestamp_fmt', "%.3f")
    nparcels_xy = kwargs.pop('nparcels_xy', (0.01, 1.05))
    no_xlabel = kwargs.pop("no_xlabel", False)
    no_ylabel = kwargs.pop("no_ylabel", False)

    # instantiating the figure object
    fkwargs = {k: v for k, v in kwargs.items() if v is not None}
    left = fkwargs.get("xmin", origin[0])
    right = fkwargs.get("xmax", origin[0] + extent[0])
    bottom = fkwargs.get("ymin", origin[1])
    top = fkwargs.get("ymax", origin[1] + extent[1])

    x_pos = ncreader.get_dataset(step=step, name="x_position")
    z_pos = ncreader.get_dataset(step=step, name="z_position")

    ind = np.argwhere((x_pos >= left - dx[0]) & (x_pos <= right + dx[0]) &
                      (z_pos >= bottom - dx[1]) & (z_pos <= top + dx[1]))
    ind = ind.squeeze()

    pos = None

    if coloring == "aspect-ratio":
        data = ncreader.get_aspect_ratio(step=step, indices=ind)
    elif coloring == "vol-distr":
        data = ncreader.get_dataset(step=step, name="volume", indices=ind)
        # 5 August 2021
        # https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
        # https://stackoverflow.com/questions/40601997/setting-discrete-colormap-corresponding-to-specific-data-range-in-matplotlib
        cmap = plt.cm.get_cmap("bwr", 2)
        bounds = [0, vmin, vmax]
        norm = cls.BoundaryNorm(bounds, cmap.N)
    else:
        data = ncreader.get_dataset(step=step, name=coloring, indices=ind)

    ells = ncreader.get_ellipses(step=step, indices=ind)

    ax.set_rasterized(True)

    ax.add_collection(ells)
    ells.set_offset_transform(ax.transData)
    ells.set_clip_box(ax.bbox)
    ells.set_alpha(1.0)
    ells.set_facecolor(cmap(norm(data)))

    ax.set_xlim([left, right])
    ax.set_ylim([bottom, top])

    # 26 May 2021
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/axis_equal_demo.html
    ax.set_aspect("equal", "box")

    if timestamp:
        add_timestamp(ax, ncreader.get_dataset(step=step, name="t"),
                      xy=timestamp_xy, fmt=timestamp_fmt)

    if nparcels:
        add_number_of_parcels(ax, len(data), xy=nparcels_xy)

    if draw_cbar:
        # 27 May 2021
        # https://stackoverflow.com/questions/29516157/set-equal-aspect-in-plot-with-colorbar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        # fig.add_axes(cax)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        cbar = plt.colorbar(sm, drawedges=False, ax=ax, cax=cax)
        # 19 Feb 2021
        # https://stackoverflow.com/questions/15003353/why-does-my-colorbar-have-lines-in-it
        cbar.set_alpha(0.75)
        cbar.solids.set_edgecolor("face")
        cbar.draw_all()

        if coloring == "aspect-ratio":
            cbar.set_label(r"$1 \leq \lambda \leq \lambda_{max}$")
        elif coloring == "vol-distr":
            # 5 August 2021
            # https://matplotlib.org/stable/gallery/ticks_and_spines/colorbar_tick_labelling_demo.html
            cbar.ax.set_yticklabels([r"0", r"$V_{min}$", r"$V_{max}$"])
        else:
            cbar.set_label(coloring)

    if not no_xlabel:
        ax.set_xlabel(get_label("$x$", units["position"]))

    if not no_ylabel:
        ax.set_ylabel(get_label("$y$", units["position"]))

    return plt.cm.ScalarMappable(cmap=cmap, norm=norm)


def plot_parcels(
    fname, step, figure="save", fmt="png", coloring="aspect-ratio", **kwargs
):
    ncreader = nc_reader()

    ncreader.open(fname)

    if not ncreader.is_parcel_file:
        raise IOError("Not a parcel output file.")

    nsteps = ncreader.get_num_steps()

    if step > nsteps - 1:
        raise ValueError("Step number exceeds limit of " + str(nsteps - 1) + ".")

    if step < 0:
        raise ValueError("Step number cannot be negative.")

    if coloring == "aspect-ratio":
        vmin = 1.0
        vmax = ncreader.get_global_attribute("lambda_max")
    elif coloring == "vol-distr":
        extent = ncreader.get_box_extent()
        ncells = ncreader.get_box_ncells()
        vcell = np.prod(extent / ncells)
        vmin = vcell / ncreader.get_global_attribute("vmin_fraction")
        vmax = vcell / ncreader.get_global_attribute("vmax_fraction")
    else:
        vmin, vmax = ncreader.get_dataset_min_max(coloring)

    plt.figure(num=step)

    _plot_parcels(plt.gca(), ncreader, step, coloring, vmin, vmax, **kwargs)

    ncreader.close()

    if figure == "return":
        return plt
    elif figure == "save":
        plt.savefig(
            "parcels_"
            + coloring
            + "_step_"
            + str(step).zfill(len(str(nsteps)))
            + "."
            + fmt,
            bbox_inches="tight",
        )
    else:
        plt.tight_layout()
        plt.show()
    plt.close()


def plot_volume_symmetry_error(fnames, figure="save", fmt="png", **kwargs):
    """
    Plot the symmetry error of the gridded volume.
    (The gridded symmetry volume is only written in debug mode.)
    """
    n = len(fnames)

    labels = kwargs.pop("labels", n * [None])

    if len(labels) < n:
        raise ValueError("Not enough labels provided.")

    colors = plt.cm.tab10(np.arange(n).astype(int))

    for i, fname in enumerate(fnames):
        ncreader = nc_reader()
        ncreader.open(fname)

        if ncreader.is_parcel_file:
            raise IOError("Not a field output file.")

        try:
            ncreader.get_dataset(0, "max_sym_vol_err")
        except:
            raise IOError("This plot is only available in debug mode.")

        nsteps = ncreader.get_num_steps()

        vmax = np.zeros(nsteps)
        t = np.zeros(nsteps)
        for step in range(nsteps):
            vmax[step] = ncreader.get_dataset(step, "max_sym_vol_err")
            t[step] = ncreader.get_dataset(step, "t")

        ncreader.close()

        plt.fill_between(
            t,
            0,
            vmax,
            color=colors[i],
            label=labels[i],
            edgecolor=colors[i],
            linewidth=0.75,
        )

    plt.grid(which="both", linestyle="dashed")
    plt.xlabel(get_label("time", units["time"]))
    plt.ylabel(r"volume symmetry error")
    plt.yscale("log")
    # plt.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))

    if not labels[0] is None:
        plt.legend(
            loc=legend_dict["loc"],
            ncol=legend_dict["ncol"],
            bbox_to_anchor=legend_dict["bbox_to_anchor"],
        )

    plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        prefix = os.path.splitext(fnames[0])[0] + "_"
        if n > 1:
            prefix = ""
        plt.savefig(prefix + "vol_sym_err." + fmt, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


def plot_rms_volume_error(fnames, figure="save", fmt="png", **kwargs):
    """
    Plot the gridded r.m.s. volume error.
    """
    n = len(fnames)

    labels = kwargs.pop("labels", n * [None])
    yscale = kwargs.pop("yscale", "linear")
    ylim = kwargs.pop("ylim", (None, None))
    no_xlabel = kwargs.pop("no_xlabel", False)
    beg = kwargs.pop("begin", None)
    end = kwargs.pop("end", None)
    tight_layout = kwargs.pop('tight_layout', True)

    if len(labels) < n:
        raise ValueError("Not enough labels provided.")

    colors = plt.cm.tab10(np.arange(n).astype(int))

    ncreader = nc_reader()
    for i, fname in enumerate(fnames):
        ncreader.open(fname)

        if ncreader.is_parcel_file:
            raise IOError("Not a field output file.")

        vrms = ncreader.get_diagnostic("rms_v")
        t = ncreader.get_diagnostic("t")
        ncreader.close()

        plt.plot(
            t[beg:end], vrms[beg:end], label=labels[i], linewidth=2, color=colors[i]
        )

    if not no_xlabel:
        plt.xlabel(get_label("time", units["time"]))
    plt.ylabel(r"r.m.s. area error")
    plt.grid(which="both", linestyle="dashed", zorder=-1)

    if not labels[0] is None:
        plt.legend(
            loc=legend_dict["loc"],
            ncol=legend_dict["ncol"],
            bbox_to_anchor=legend_dict["bbox_to_anchor"],
        )
    plt.yscale(yscale)

    if yscale == "linear":
        plt.ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))
    plt.ylim(ylim)

    if tight_layout:
        plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        plt.savefig("rms_vol_err." + fmt, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


def plot_max_volume_error(fnames, figure="save", fmt="png", **kwargs):
    """
    Plot the gridded absolute volume error (normalised with
    cell volume).
    """
    n = len(fnames)

    labels = kwargs.pop("labels", n * [None])
    no_xlabel = kwargs.pop("no_xlabel", False)
    beg = kwargs.pop("begin", None)
    end = kwargs.pop("end", None)
    tight_layout = kwargs.pop('tight_layout', True)

    if len(labels) < n:
        raise ValueError("Not enough labels provided.")

    colors = plt.cm.tab10(np.arange(n).astype(int))

    ncreader = nc_reader()
    for i, fname in enumerate(fnames):
        ncreader.open(fname)

        if ncreader.is_parcel_file:
            raise IOError("Not a field output file.")

        vmax = ncreader.get_diagnostic("max absolute normalised volume error")
        t = ncreader.get_diagnostic("t")
        ncreader.close()

        plt.plot(
            t[beg:end], vmax[beg:end], label=labels[i], linewidth=2, color=colors[i]
        )

    plt.ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))

    if not no_xlabel:
        plt.xlabel(get_label("time", units["time"]))
    plt.ylabel(r"max normalised volume error")
    plt.grid(linestyle="dashed", zorder=-1)

    if not labels[0] is None:
        plt.legend(
            loc=legend_dict["loc"],
            ncol=legend_dict["ncol"],
            bbox_to_anchor=legend_dict["bbox_to_anchor"],
        )

    if tight_layout:
        plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        plt.savefig("max_normalised_vol_err." + fmt, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


def plot_parcel_profile(fnames, figure="save", fmt="png", **kwargs):
    """
    Plot the mean and standard deviation of the parcel aspect ratio.
    """
    n = len(fnames)

    labels = kwargs.pop("labels", n * [None])
    dset = kwargs.pop("dset", "aspect-ratio")
    no_xlabel = kwargs.pop("no_xlabel", False)
    beg = kwargs.pop("begin", None)
    end = kwargs.pop("end", None)
    tight_layout = kwargs.pop('tight_layout', True)

    colors = plt.cm.tab10(np.arange(n).astype(int))

    if len(labels) < n:
        raise ValueError("Not enough labels provided.")

    ncreader = nc_reader()

    lmax = 0

    for i, fname in enumerate(fnames):

        ncreader.open(fname)

        if not ncreader.is_parcel_file:
            raise IOError("Not a parcel output file.")

        nsteps = ncreader.get_num_steps()

        data_mean = np.zeros(nsteps)
        data_std = np.zeros(nsteps)
        t = np.zeros(nsteps)

        for step in range(nsteps):

            data = None

            if dset == "aspect-ratio":
                data = ncreader.get_aspect_ratio(step)
            else:
                data = ncreader.get_dataset(step, dset)

            if dset == "volume":
                extent = ncreader.get_box_extent()
                ncells = ncreader.get_box_ncells()
                vcell = np.prod(extent / ncells)
                data /= vcell

            data_mean[step] = data.mean()
            data_std[step] = data.std()

            t[step] = ncreader.get_dataset(step, "t")

        if dset == "aspect-ratio":
            lmax = max(lmax, ncreader.get_global_attribute("lambda_max"))

        ncreader.close()

        plt.plot(t[beg:end], data_mean[beg:end], label=labels[i], color=colors[i])
        plt.fill_between(
            t[beg:end],
            data_mean[beg:end] - data_std[beg:end],
            data_mean[beg:end] + data_std[beg:end],
            alpha=0.5,
            color=colors[i],
        )

        print(fname, data_mean.mean(), data_std.mean())

    if not no_xlabel:
        plt.xlabel(get_label("time", units["time"]))
    plt.grid(linestyle="dashed", zorder=-1)

    if dset == "aspect-ratio":
        plt.ylabel(r"aspect ratio $\lambda$")
        plt.text(t[10], 0.92 * lmax, r"$\lambda\le\lambda_{max} = " + str(lmax) + "$")
        plt.axhline(lmax, linestyle="dashed", color="black")
    elif dset == "volume":
        plt.ylabel(r"parcel volume / $V_{g}$")
        # plt.axhline(1.0, linestyle='dashed', color='black',
        # label=r'cell volume $V_{g}$')
    else:
        plt.ylabel(r"parcel " + dset)

    if not labels[0] is None:
        plt.legend(
            loc=legend_dict["loc"],
            ncol=legend_dict["ncol"],
            bbox_to_anchor=legend_dict["bbox_to_anchor"],
        )

    if tight_layout:
        plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        prefix = os.path.splitext(fnames[0])[0] + "_"
        if n > 1:
            prefix = ""
        plt.savefig(prefix + "parcel_" + dset + "_profile." + fmt, bbox_inches="tight")
    else:
        plt.show()

    plt.close()


def plot_parcel_stats_profile(fnames, figure="save", fmt="png", **kwargs):
    """
    Plot parcel statistics
    """
    n = len(fnames)

    labels = kwargs.pop("labels", n * [None])
    dset = kwargs.pop("dset", "aspect-ratio")
    no_xlabel = kwargs.pop("no_xlabel", False)
    beg = kwargs.pop("begin", None)
    end = kwargs.pop("end", None)

    if dset == "aspect-ratio":
        dset = "aspect ratio"

    colors = plt.cm.tab10(np.arange(n).astype(int))

    if len(labels) < n:
        raise ValueError("Not enough labels provided.")

    ncreader = nc_reader()

    lmax = 0

    for i, fname in enumerate(fnames):

        ncreader.open(fname)

        if not ncreader.is_parcel_stats_file:
            raise IOError("Not a parcel diagnostic output file.")

        nsteps = ncreader.get_num_steps()

        data_mean = np.zeros(nsteps)
        data_std = np.zeros(nsteps)
        t = np.zeros(nsteps)

        for step in range(nsteps):
            t[step] = ncreader.get_dataset(step, "t")
            data_mean[step] = ncreader.get_dataset(step, "avg " + dset)
            data_std[step] = ncreader.get_dataset(step, "std " + dset)

        if dset == "aspect ratio":
            lmax = max(lmax, ncreader.get_global_attribute("lambda_max"))

        ncreader.close()

        plt.plot(t[beg:end], data_mean[beg:end], label=labels[i], color=colors[i])
        plt.fill_between(
            t[beg:end],
            data_mean[beg:end] - data_std[beg:end],
            data_mean[beg:end] + data_std[beg:end],
            alpha=0.5,
            color=colors[i],
        )

    if not no_xlabel:
        plt.xlabel(get_label("time", units["time"]))
    plt.grid(linestyle="dashed", zorder=-1)

    if dset == "aspect-ratio":
        plt.ylabel(r"aspect ratio $\lambda$")
        plt.text(t[10], 0.95 * lmax, r"$\lambda\le\lambda_{max} = " + str(lmax) + "$")
        plt.axhline(lmax, linestyle="dashed", color="black")
    elif dset == "volume":
        plt.ylabel(r"parcel volume / $V_{g}$")
        # plt.axhline(1.0, linestyle='dashed', color='black',
        # label=r'cell volume $V_{g}$')
    else:
        plt.ylabel(r"parcel " + dset)

    if not labels[0] is None:
        plt.legend(
            loc=legend_dict["loc"],
            ncol=legend_dict["ncol"],
            bbox_to_anchor=legend_dict["bbox_to_anchor"],
        )

    plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        prefix = os.path.splitext(fnames[0])[0] + "_"
        if n > 1:
            prefix = ""
        dset = dset.replace(" ", "_")
        plt.savefig(prefix + "parcel_" + dset + "_profile." + fmt, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


def plot_parcel_number(fnames, figure="save", fmt="png", **kwargs):
    """
    Plot the number of parcels in simulation.
    """
    labels = kwargs.pop("labels", None)
    no_xlabel = kwargs.pop("no_xlabel", False)
    beg = kwargs.pop("begin", None)
    end = kwargs.pop("end", None)
    tight_layout = kwargs.pop('tight_layout', True)

    if labels is None:
        labels = [None] * len(fnames)

    for i, fname in enumerate(fnames):

        ncreader = nc_reader()
        ncreader.open(fname)

        if not ncreader.is_parcel_file:
            raise IOError("Not a parcel output file.")

        nsteps = ncreader.get_num_steps()

        nparcels = np.zeros(nsteps)
        t = np.zeros(nsteps)

        for step in range(nsteps):
            nparcels[step] = ncreader.get_num_parcels(step)
            t[step] = ncreader.get_dataset(step, "t")

        ncreader.close()

        plt.plot(t[beg:end], nparcels[beg:end], label=labels[i])

    plt.grid(linestyle="dashed", zorder=-1)

    if not labels[0] is None:
        plt.legend(
            loc=legend_dict["loc"],
            ncol=min(len(labels), legend_dict["ncol"]),
            bbox_to_anchor=legend_dict["bbox_to_anchor"],
        )

    if not no_xlabel:
        plt.xlabel(get_label("time", units["time"]))
    plt.ylabel(r"parcel count")

    if tight_layout:
        plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        plt.savefig("parcel_number_profile." + fmt, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


def plot_small_parcel_number(fnames, figure="save", fmt="png", **kwargs):
    """
    Plot the number of small parcels in simulation.
    """
    labels = kwargs.pop("labels", None)
    no_xlabel = kwargs.pop("no_xlabel", False)
    beg = kwargs.pop("begin", None)
    end = kwargs.pop("end", None)
    tight_layout = kwargs.pop('tight_layout', True)

    if labels is None:
        labels = [None] * len(fnames)

    for i, fname in enumerate(fnames):

        ncreader = nc_reader()
        ncreader.open(fname)

        if not ncreader.is_parcel_stats_file:
            raise IOError("Not a parcel diagnostic output file.")

        nsteps = ncreader.get_num_steps()

        nparcels = np.zeros(nsteps)
        nsmall = np.zeros(nsteps)
        t = np.zeros(nsteps)

        for step in range(nsteps):
            nparcels[step] = ncreader.get_dataset(step, "n_parcels")
            nsmall[step] = ncreader.get_dataset(step, "n_small_parcel")
            t[step] = ncreader.get_dataset(step, "t")

        ncreader.close()

        plt.plot(
            t[beg:end], nsmall[beg:end] / nparcels[beg:end] * 100.0, label=labels[i]
        )

    plt.grid(linestyle="dashed", zorder=-1)

    if not labels[0] is None:
        plt.legend(
            loc=legend_dict["loc"],
            ncol=min(len(labels), legend_dict["ncol"]),
            bbox_to_anchor=legend_dict["bbox_to_anchor"],
        )

    if not no_xlabel:
        plt.xlabel(get_label("time", units["time"]))
    plt.ylabel(r"small parcel fraction (\%)")

    if tight_layout:
        plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        plt.savefig("parcel_small_number_profile." + fmt, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


def plot_power_spectrum(fnames, figure="save", fmt="png", **kwargs):
    """
    Reads in a power spectrum file generated by the standalone
    program genspec.
    """
    n = len(fnames)

    labels = kwargs.pop("labels", n * [None])
    yscale = kwargs.pop("yscale", "linear")
    no_xlabel = kwargs.pop("no_xlabel", False)

    if len(labels) < n:
        raise ValueError("Not enough labels provided.")

    colors = plt.cm.tab10(np.arange(n).astype(int))

    for i, fname in enumerate(fnames):

        if not "_spectrum.asc" in fname:
            raise IOError("Not a spectrum file.")

        k, spec = np.loadtxt(fname, skiprows=3, unpack=True)
        plt.loglog(k, spec, label=labels[i])

    plt.grid(which="both", linestyle="dashed")

    if not no_xlabel:
        plt.xlabel(get_label(r"$k$", units["wavenumber"]))
    plt.ylabel(get_label(r"$P(k)$", units["power"]))

    if not labels[0] is None:
        plt.legend(
            loc=legend_dict["loc"],
            ncol=legend_dict["ncol"],
            bbox_to_anchor=legend_dict["bbox_to_anchor"],
        )

    plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        prefix = os.path.splitext(fnames[0])[0] + "_"
        if n > 1:
            prefix = ""
        plt.savefig(prefix + "power_spectrum." + fmt, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


def plot_parcels_per_cell(fnames, figure="save", fmt="png", **kwargs):
    """
    Plot the mean and standard deviation of the number of
    parcels per cell
    """
    n = len(fnames)

    labels = kwargs.pop("labels", n * [None])
    add_minmax = kwargs.pop("add_minmax", True)
    no_xlabel = kwargs.pop("no_xlabel", False)
    beg = kwargs.pop("begin", None)
    end = kwargs.pop("end", None)

    if len(labels) < n:
        raise ValueError("Not enough labels provided.")

    colors = plt.cm.tab10(np.arange(n).astype(int))

    for i, fname in enumerate(fnames):
        ncreader = nc_reader()
        ncreader.open(fname)

        if not ncreader.is_field_stats_file:
            raise IOError("Not a field diagnostic output file.")

        nsteps = ncreader.get_num_steps()

        n_avg = np.zeros(nsteps)

        if add_minmax:
            n_min = np.zeros(nsteps)
            n_max = np.zeros(nsteps)

        t = np.zeros(nsteps)

        for step in range(nsteps):
            n_avg[step] = ncreader.get_dataset(step, "avg_npar")
            t[step] = ncreader.get_dataset(step, "t")

            if add_minmax:
                n_min[step] = ncreader.get_dataset(step, "min_npar")
                n_max[step] = ncreader.get_dataset(step, "max_nar")

        ncreader.close()

        plt.plot(t[beg:end], n_avg[beg:end], color=colors[i], label=labels[i])

        if add_minmax:
            plt.fill_between(
                t[beg:end],
                n_min[beg:end],
                n_max[beg:end],
                color=colors[i],
                alpha=0.5,
                edgecolor=None,
            )

    if not no_xlabel:
        plt.xlabel(get_label("time", units["time"]))
    plt.ylabel(r"number of parcels/cell")
    plt.grid(which="both", linestyle="dashed")

    if not labels[0] is None:
        plt.legend(
            loc=legend_dict["loc"],
            ncol=legend_dict["ncol"],
            bbox_to_anchor=legend_dict["bbox_to_anchor"],
        )

    plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        prefix = os.path.splitext(fnames[0])[0] + "_"
        if n > 1:
            prefix = ""
        plt.savefig(prefix + "number_of_parcels_per_cell." + fmt, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


def plot_energy(fname, figure="save", fmt="png", **kwargs):
    """
    Plot the kinetic, potential and total energy.
    """
    no_xlabel = kwargs.pop("no_xlabel", False)
    beg = kwargs.pop("begin", None)
    end = kwargs.pop("end", None)

    ncreader = nc_reader()
    ncreader.open(fname)

    if not ncreader.is_parcel_stats_file:
        raise IOError("Not a parcel diagnostic output file.")

    nsteps = ncreader.get_num_steps()

    pe = np.zeros(nsteps)
    ke = np.zeros(nsteps)
    te = np.zeros(nsteps)
    t = np.zeros(nsteps)

    for step in range(nsteps):
        pe[step] = ncreader.get_dataset(step, "pe")
        ke[step] = ncreader.get_dataset(step, "ke")
        te[step] = ncreader.get_dataset(step, "te")
        t[step] = ncreader.get_dataset(step, "t")

    ncreader.close()

    plt.plot(t[beg:end], pe[beg:end], label=r"$P$")
    plt.plot(t[beg:end], ke[beg:end], label=r"$K$")
    plt.plot(t[beg:end], te[beg:end], label=r"$P+K$")

    if not no_xlabel:
        plt.xlabel(get_label("time", units["time"]))
    plt.ylabel(get_label("energy", units["energy"]))
    plt.grid(which="both", linestyle="dashed")

    plt.legend(
        loc=legend_dict["loc"],
        ncol=legend_dict["ncol"],
        bbox_to_anchor=legend_dict["bbox_to_anchor"],
    )

    plt.tight_layout()

    if figure == "return":
        return plt
    elif figure == "save":
        prefix = os.path.splitext(fname)[0]
        prefix = prefix.split("parcel_stats")[0]
        plt.savefig(prefix + "energy." + fmt, bbox_inches="tight")
    else:
        plt.show()
    plt.close()
