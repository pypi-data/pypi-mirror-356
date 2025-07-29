import matplotlib.pyplot as plt
import numpy as np


# ----------------------------------------
# -- draw hist function (a la ROOT)
# ----------------------------------------
def draw(x, y, xerr=None, yerr=None, option='hist', color=None, ls='-', marker='.', legend=''):
    """
    Draws  x, y as histograms or graph if need be)
    :param x: x axis (can be a bining, ie with a len(x) = len(y) + 1)
    :param y: y axis
    :param xerr: np.array containing the x error (auto if histogram)
    :param yerr: np.array containing the y error
    :param option: a la ROOT
    :param color: color
    :param ls: linestyle (matplotlib)
    :param marker: marker style (matplotlib)
    :param legend: label to be used in the legend
    :return:
    """

    x_hist = x.copy()
    if len(x) == len(y) + 1:
        # histogram case
        x_hist = x.copy()
        xerr = 0.5 * (x[1:] - x[:-1])
        x = 0.5 * (x[:-1] + x[1:])

    fill = False
    if 'hist' in option or 'H' in option or 'fill' in option:
        if 'fill' in option:
            fill = True
        x_hist = np.array([x_hist, x_hist]).T.flatten()
        y_hist = np.array([y, y]).T.flatten()
        y_hist = np.concatenate([[0], y_hist, [0]])

        p = plt.plot(x_hist, y_hist, color=color, linewidth=2, label=legend, linestyle=ls)
        if fill:
            color = plt.gca().lines[-1].get_color()
            plt.bar(x, y, width=xerr * 2, color=color, alpha=0.5)

    elif 'err0' in option or 'E0' in option:
        plt.errorbar(x, y, xerr=xerr, yerr=0,
                     color=color, linestyle='', marker=marker, markersize=6, label=legend)

    elif 'err1' in option or 'E1' in option:
        plt.errorbar(x, y, xerr=xerr, yerr=0,
                     color=color, linestyle='', marker=marker, markersize=6, label=legend)

        x = np.concatenate([[(3*x[0]-x[1])/2], x, [(3*x[-1]-x[-2])/2.]])
        y = np.concatenate([[y[0]], y, [y[-1]]])
        yerr = np.concatenate([[yerr[0]], yerr, [yerr[-1]]])
        color = plt.gca().lines[-1].get_color()
        plt.fill_between(x, y - yerr, y + yerr,
                         step='mid', color=color, alpha=0.7, linewidth=0)

    elif 'err' in option or 'E' in option:
        y = np.where(y == 0, np.nan, y)
        plt.errorbar(x, y, xerr=xerr, yerr=yerr,
                     color=color, linestyle='', marker=marker, markersize=6, label=legend)

    # plt.axhline(color='k', ls='-')
