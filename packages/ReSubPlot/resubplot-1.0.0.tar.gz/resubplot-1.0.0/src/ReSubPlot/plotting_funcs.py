"""This module has the functions that allow the replotting of several existing
Figure objects into a new Figure with subplots, while sharing axes, ylabels,
yticks, etc. on each row."""

#pylint: disable=line-too-long

from ReSubPlot.layout import create_figure, legends_only_last_subplot, labels_only_last_subplot, set_common_ylims, add_column_titles, align_ylabels

def master_plot(mat_fig, list_sites, pad=0.03, save_plots=None):
    """ Function takes a list of figure objects and 
    prints them into subplots
    
    Parameters
    ----------
    mat_fig : list of Figure
        List of original figures to be plotted in a subplots()
        in the format of the list
        It has to be an m*n list
        [[fig_1_1, ..., fig_1_n],
         [fig_2_1, ..., fig_2_n],
         ...
        [fig_m_1, ..., fig_m_n]]
    list_sites : list
        List of sites (length n), 1 site per column
        will be used to label each column
    pad : float
        padding between subplots, suggest 0.03
    save_plots : string, optional
        If a name is passed, figure will be saved to PDF with the name
        f'{save_plots}.pdf'

    Returns
    -------
    fig : Figure
        figure with subplots
    tens : list
        list in the subplot shape that indicates the numbering of axes 
        for each subplot
    """
    fig, tens = create_figure(mat_fig, list_sites, pad)
    fig = legends_only_last_subplot(fig, tens)
    fig = labels_only_last_subplot(fig, tens)
    fig = set_common_ylims(fig, tens)
    fig = add_column_titles(fig, tens, list_sites)
    fig = align_ylabels(fig, tens)

    if save_plots:
        fig.savefig(f'{save_plots}.pdf', bbox_inches='tight')

    return fig, tens
