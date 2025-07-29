"""This module has all the functions that extract legend information from an
existing Figure object."""

#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace

import pickle
import matplotlib
import matplotlib.pyplot as plt

def get_all_legends_fig(fig):
    """ Function takes a figure object and extracts all legends
    
    Parameters
    ----------
    fig : Figure

    Returns
    -------
    handles : list
        All legend handles
    labels : list
        All legend labels
    """

    handles = []
    labels = []
    for ax in fig.axes:
        handles += get_all_legends_ax(ax)[0]
        labels += get_all_legends_ax(ax)[1]

    return handles, labels

def get_all_legends_ax(ax):
    """ Function takes an axis object and extracts all legends
    
    Parameters
    ----------
    ax : Axis

    Returns
    -------
    handles : list
        All legend handles
    labels : list
        All legend labels
    """

    handles, labels = ax.get_legend_handles_labels()

    return handles, labels

def isolate_legend(fig_no_legend, save_plots=None):
    """ Function takes an original figure object and creates a copy of it,
    another copy without the legend, and a legend object only.
    The user has the ability to save all three figures to PDF too.
    
    Parameters
    ----------
    fig_no_legend : matplotlib.figure.Figure
        Original figure
    save_plots : string, optional
        If a name is passed, figure will be saved to PDF with the name
        f'{save_plots}.pdf'

    Returns
    -------
    fig_with_legend : matplotlib.figure.Figure
        this is the original figure, with the legend
    fig_no_legend : matplotlib.figure.Figure
        original figure stripped of its legend
    legend : matplotlib.legend.Legend
        legend of the original plot
    """
    fig_with_legend = pickle.dumps(fig_no_legend)
    list_idx_ax_leg = []
    for i, ax in enumerate(fig_no_legend.axes):
        if ax.get_legend():
            list_idx_ax_leg.append(i)

    if len(list_idx_ax_leg)==1:
        ax = fig_no_legend.axes[0]
        legend = get_all_legends_ax(ax)
        handles, labels = legend
    else:
        if len(list_idx_ax_leg)==0:
            legend = next((a for a in fig_no_legend.get_children() if isinstance(a, matplotlib.legend.Legend)), None)
            if legend:
                handles = legend.legend_handles
                labels = [t.get_text() for t in legend.get_texts()]
            else:
                handles, labels = [], []
        else:
            handles, labels = [], []
            
    # Remove all legends from axes (including twinx)
    for ax in fig_no_legend.axes:
        for child in ax.get_children():
            if isinstance(child, matplotlib.legend.Legend):
                child.remove()
    if len(list_idx_ax_leg)==0:
        if legend:
            legend.remove()

    # Remove figure-level legends from fig.artists
    fig_no_legend.artists = [a for a in fig_no_legend.artists if not isinstance(a, matplotlib.legend.Legend)]

    # Also remove figure-level legends from top-level children (paranoid mode)
    fig_no_legend._axstack.as_list()  # Ensure figure state is registered correctly
    for child in fig_no_legend.get_children():
        if isinstance(child, matplotlib.legend.Legend):
            child.remove()

    fig_with_legend = pickle.loads(fig_with_legend)


    if save_plots:
        fig_legend = plt.figure()
        fig_legend.legend(handles, labels, loc='center')
        fig_legend.savefig(f'{save_plots}_legend_only.pdf', bbox_inches='tight')
        fig_with_legend.savefig(f'{save_plots}_legend_on.pdf', bbox_inches='tight')
        fig_no_legend.savefig(f'{save_plots}_legend_off.pdf', bbox_inches='tight')

    return fig_with_legend, fig_no_legend, legend
