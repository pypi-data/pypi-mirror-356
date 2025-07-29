import os
import matplotlib
import matplotlib.pyplot as plt
from typing import Union, Sequence, Tuple

import numpy as np
import pandas as pd

from .plotter import draw

# import the style defined in the package mplstyle
plt.style.use(os.path.dirname(__file__) + '/resources/fStyle.mplstyle')


def polish_axis(ax=None, x_title='', y_title='',
                x_range: Union[Sequence[float], Tuple[float]] = (),
                y_range: Union[Sequence[float], Tuple[float]] = (),
                cms=False, prelim=False, simu=False, text=None,
                year: int = 0, lumi=0.0, com=13.6,
                **kwargs):
    """

    :param ax: matplotlib axis to decorate
    :param x_title: (str) x-axis title
    :param y_title: (str) y-axis title
    :param x_range: x-axis range ([a, b] or (a, b) or (a,))
    :param y_range: x-axis range ([a, b] or (a, b) or (a,))
    :param leg_title: legend title ('' to just display the legend without title)
    :param leg_loc: location of the legend (see matplotlib, None = auto)
    :param cms: (bool) add cms decoration
    :param prelim: (bool) add Preliminary
    :param simu: (bool) add Simulation
    :param text: (str) additional text to add to the plot
    :param year: (int) add the year
    :param lumi: (float) add the luminosity
    :param com: (float) center of mass energy
    :return:
    """

    if ax is None:
        ax = plt.gca()

    # Extract legend kwargs
    legend_kwargs = {
        k[4:]: v for k, v in kwargs.items() if k.startswith('leg_')
    }

    if legend_kwargs:
        leg = ax.legend(**legend_kwargs)
        if 'title_fontsize' not in legend_kwargs:
            plt.setp(leg.get_title(), fontsize='x-large')

    if len(x_range) > 0:
        ax.set_xlim(*x_range)
    if len(y_range) > 0:
        ax.set_ylim(*y_range)

    if len(y_title) > 0:
        ax.set_ylabel(y_title, ha='right', y=1)
    if len(x_title) > 0:
        ax.set_xlabel(x_title, ha='right', x=1)

    if not cms:
        return

    logo = ['CMS']
    if simu:
        text = 'Simulation'
    if prelim:
        text = 'Preliminary' 
    if text:
        logo.append(f' ${text}$')
    if year:
        logo.append(f' {year}')
    logo = ''.join(logo)

    ax.set_title(logo, loc='left', fontweight='bold')

    if lumi :
        ax.set_title(f'{lumi:2.1f} fb$^{{-1}}$ ({com} TeV)', loc='right', fontsize=15.0)


def last_color(ax=None):
    """
    Return the last color used on the axis
    :param ax: matplotlib axis (None == current axis)
    :return:
    """
    if ax is None:
        ax = plt.gca()
    return ax.get_lines()[-1].get_color()


def show():
    """
    short for plt.show()
    :return:
    """
    plt.show()


def heatmap(data: Union[np.ndarray, pd.DataFrame], ax=None,
            colorbar=True, grid=False, text=False, valfmt="{x:.2f}", **kwargs):

    """
    Supply a heatmap plotter
    :param data: data to display
    :param ax: axis
    :param colorbar: add a color bar
    :param grid: add a grid
    :param text: print the bin content
    :param valfmt: formatter for the content
    :param kwargs: arguments to pass to imshow to display the map

    :return:
    """

    # data as DataFrame
    data = pd.DataFrame(data)

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = None
    if colorbar:
        cbar = ax.figure.colorbar(im, ax=ax)
        # cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=data.columns)
    ax.set_yticks(np.arange(data.shape[0]), labels=data.index)

    # Rotate the tick labels and set their alignment.
    # plt.setp(ax.get_xticklabels(), rotation=-30, ha="right", rotation_mode="anchor")
    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)

    if grid:
        # Turn spines off and create white grid.
        ax.spines[:].set_visible(False)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    #        ax.tick_params(which="minor", top=False, left=False)

    if text:
        kw = dict(horizontalalignment="center", verticalalignment="center")
        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                text = im.axes.text(j, i, valfmt(data.iloc[i, j], None), **kw)

    return im, cbar
