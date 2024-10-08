import matplotlib as mpl
from tools.mpl_style import *
from tools.units import *

def remove_xticks(ax):
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

def remove_yticks(ax):
    ax.tick_params(axis='y', which='both', right=False, left=False)

def add_annotation(ax, label, xy, **kwargs):
    bbox = dict(boxstyle="round", facecolor="wheat", linewidth=0.5)
    ax.annotate(label, xy=xy, xycoords="axes fraction", bbox=bbox, **kwargs)

def add_timestamp(plt, time, xy=(0.75, 1.05), fmt="%.3f", **kwargs):
    # 29. Dec 2020
    # https://matplotlib.org/3.1.1/gallery/pyplots/annotate_transform.html#sphx-glr-gallery-pyplots-annotate-transform-py
    # https://stackoverflow.com/questions/7045729/automatically-position-text-box-in-matplotlib
    # https://matplotlib.org/3.1.0/gallery/recipes/placing_text_boxes.html
    bbox = dict(boxstyle="round", facecolor="wheat", linewidth=0.5)

    label = r"t = " + fmt % (time)
    if units['time'] is not None:
        label = r"t = " + fmt % (time) + units["time"]

    plt.annotate(
        label, xy=xy, xycoords="axes fraction", bbox=bbox, **kwargs
    )


def add_number_of_parcels(plt, num, xy=(0.01, 1.05)):
    bbox = dict(boxstyle="round", facecolor="wheat", linewidth=0.5)
    plt.annotate(
        r'no. parcels = %7.0f' % (num),
        xy=xy,
        xycoords="axes fraction",
        bbox=bbox,
    )


def add_box(plt, label, value, unit="", xy=(0.01, 1.05), fmt="%1.3f"):
    bbox = dict(boxstyle="round", facecolor="wheat", linewidth=0.5)


    text = label + " = " + fmt % (value) + unit
    plt.annotate(
        text, xy=xy, xycoords="axes fraction", bbox=bbox
    )


# 25 June 2021
# https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html#sphx-glr-gallery-pie-and-polar-charts-pie-and-donut-labels-py
def get_autopct(pct, allvals):
    import numpy as np

    absolute = pct / 100.0 * np.sum(allvals)
    return r"{:.2f}$\%$\n({:.1f} s)".format(pct, absolute)
