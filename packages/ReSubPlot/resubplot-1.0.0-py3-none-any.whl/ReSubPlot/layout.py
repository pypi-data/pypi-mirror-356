"""This module has all the functions that extract information from an
existing Figure object."""

#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=invalid-name

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll

def recover_figsize(old_fig):
    """ Function takes a figure object and extracts size in inches
    
    Parameters
    ----------
    old_fig : Figure
        original figure 

    Returns
    -------
    size of the figure in inches
    """
    return old_fig.get_size_inches()

def recover_axis_position(old_ax, new_ax):
    """ Function takes an axis object and
    recovers x and y axis position

    Parameters
    ----------
    old_ax : matplotlib.axes._axes.Axes
        Axis of the original figure
    new_ax : matplotlib.axes._axes.Axes
        Axis of the new figure

    Returns
    -------
    x and y axis positions
    """
    new_ax.set_position(old_ax.get_position())

def sharing_axis(new_ax_og, old_fig, old_ax):
    """ Function takes an axis object and
    finds how to best create the new axis

    Parameters
    ----------
    new_ax_og : matplotlib.axes._axes.Axes
        Axis of the new figure
    old_fig : Figure
        original figure 
    old_ax : matplotlib.axes._axes.Axes
        Axis of the original figure
        
    Returns
    -------
    new_ax : matplotlib.axes._axes.Axes
        Axis of the new figure
    """
    # when looping through axis, finds out whether the current axis is the
    # same as the first axis of the list
    if old_ax == old_fig.axes[0]:
        new_ax = new_ax_og
        # if not, figures whether they share x or y axis and recovers the position
    else:
        if old_fig.axes[0].get_shared_x_axes().joined(old_fig.axes[0], old_ax):
            new_ax = new_ax_og.twinx()
        if old_fig.axes[0].get_shared_y_axes().joined(old_fig.axes[0], old_ax):
            new_ax = new_ax_og.twiny()
        # else:
        #     new_ax = new_ax_og
        # recover_axis_position(old_ax, new_ax)
    # new_ax.set_position(new_ax_og.get_position())
    return new_ax

def recover_Line2D(old_ax, new_ax):
    """ Function takes an axis and extracts all 2d lines

    Parameters
    ----------
    old_ax : matplotlib.axes._axes.Axes
        Axis of the original figure
    new_ax : matplotlib.axes._axes.Axes
        Axis of the new figure
    """
    for line in old_ax.get_lines():
        new_ax.plot(
            line.get_xdata(), 
            line.get_ydata(), 
            label=line.get_label(),
            color=line.get_color(),
            linestyle=line.get_linestyle()
        )

def recover_axhline(old_ax, new_ax):
    """ Function takes an axis and extracts all axlines

    Parameters
    ----------
    old_ax : matplotlib.axes._axes.Axes
        Axis of the original figure
    new_ax : matplotlib.axes._axes.Axes
        Axis of the new figure
    """
    for line in old_ax.get_lines():
        # Check if the line is a horizontal line (constant y-value)
        y_data = np.array(line.get_ydata())  # Convert to numpy array if it's not already
        if y_data.size == 2:  # If it's a horizontal line (constant y-value)
            y_value = y_data[0]
            
            # Recover the axhline using axhline in new_ax
            new_ax.axhline(
                y=y_value,
                color=line.get_color(),
                linestyle=line.get_linestyle(),
                linewidth=line.get_linewidth(),
                label=line.get_label()  # If you want to recover the label as well
            )

def recover_fill_between(old_ax, new_ax):
    """ Function takes an axis and extracts all fill_between

    Parameters
    ----------
    old_ax : matplotlib.axes._axes.Axes
        Axis of the original figure
    new_ax : matplotlib.axes._axes.Axes
        Axis of the new figure
    """
    for poly in old_ax.collections:
        if isinstance(poly, mcoll.PolyCollection):
            # Each PolyCollection could have multiple polygons
            for path in poly.get_paths():
                verts = path.vertices
                x_pre = verts[:, 0]
                x = x_pre[1:int(len(x_pre)/2)]
                y = verts[:, 1]
                y1 = y[1:int(len(y)/2)]
                y2 = y[int(len(y)/2)+1:-1][::-1]
                new_ax.fill_between(
                    x, y1=y1, y2=y2, 
                    color=poly.get_facecolor()[0], 
                    alpha=poly.get_alpha()
                )

def recover_axis_formatting(old_ax, new_ax):
    """ Function takes an axis and recovers axis formatting

    Parameters
    ----------
    old_ax : matplotlib.axes._axes.Axes
        Axis of the original figure
    new_ax : matplotlib.axes._axes.Axes
        Axis of the new figure
    """
    # Recover axis labels and title from the original axes
    new_ax.set_xlabel(old_ax.get_xlabel())
    new_ax.set_ylabel(old_ax.get_ylabel())
    new_ax.set_title(old_ax.get_title())

    # Recover tick labels (if any custom ticks were used)
    new_ax.set_xticks(old_ax.get_xticks())
    # new_ax.set_yticks(old_ax.get_yticks())
    new_ax.set_xticklabels(old_ax.get_xticklabels())
    # new_ax.set_yticklabels(old_ax.get_yticklabels())

    # Recover x and y limits from the original axes
    new_ax.set_xlim(old_ax.get_xlim())
    new_ax.set_ylim(old_ax.get_ylim())

def recover_legend(old_ax, new_ax):
    """ Function takes an axis and recovers legend

    Parameters
    ----------
    old_ax : matplotlib.axes._axes.Axes
        Axis of the original figure
    new_ax : matplotlib.axes._axes.Axes
        Axis of the new figure
    """
    if old_ax.get_legend() is not None:
        new_ax.legend()

def print_into_row_subplots(temp_fig_list, new_fig, pad):
    """ Function takes a list of figure objects and 
    prints them into subplots
    
    Parameters
    ----------
    temp_fig_list : list of Figure
        List of original figures to be plotted in a subplots()
        in the format of the list
    new_fig : Figure
        New figure where the subplots will be created
    pad : float
        padding between subplots, suggest 0.05

    Returns
    -------
    tens : list
        list in the subplot shape that indicates the numbering of axes 
        for each subplot
    """
    num_ax = 0
    tens = []
    (nrows, ncols) = np.array(temp_fig_list).shape
    for i,m in enumerate(temp_fig_list):
        mat = []
        for j,f in enumerate(m):
            vec=[]
            ax = new_fig.add_subplot(nrows, ncols, i*ncols+j+1)
            # print(nrows, ncols, i*ncols+j+1, i*ncols+j+1)
            plot_same_new_figure(f, ax)
            num_new_ax = len(new_fig.axes)-num_ax
            for n in range(num_ax,num_ax+num_new_ax):
                vec.append(n)
                new_fig.axes[n].set_position([(j+pad)/ncols, (i+pad)/nrows, (1-2*pad)/ncols, (1-2*pad)/nrows])
            num_ax = len(new_fig.axes)
            mat.append(vec)
        tens.append(mat)
        # !!!!!!!!!!!!!!! NEED THIS !!!!!!!!!!!!!!!
    tens = tens[::-1]

    return tens

def create_figure(mat_fig, list_sites, pad):
    """ Function takes a list of figure objects and 
    prints them into subplots
    
    Parameters
    ----------
    mat_fig : list of Figure
        List of original figures to be plotted in a subplots()
        in the format of the list
        It has to be an n*m list [[fig1, ..., fign], [], ..., []]
    list_sites : list
        List of sites, 1 site per column
        will be used to label each column
    pad : float
        padding between subplots, suggest 0.03

    Returns
    -------
    fig : Figure
        figure with subplots
    tens : list
        list in the subplot shape that indicates the numbering of axes 
        for each subplot
    """
    temp_fig_list = np.array(mat_fig).reshape(-1,len(list_sites))
    # !!!!!!!!!!!!!!! I DO NOT UNDERSTAND !!!!!!!!!!!!!!!
    # For some reason, the rows are swapped so I need to unswap here
    # but it complicates a few other things, especially the definition of 'tens' 
    temp_fig_list = temp_fig_list[::-1]
    (_, ncols) = temp_fig_list.shape
    fig = plt.figure(figsize=(ncols*np.max([f[0].get_size_inches()[0] for f in temp_fig_list]),
                              np.sum([f[0].get_size_inches()[1] for f in temp_fig_list])))
    tens = print_into_row_subplots(temp_fig_list, fig, pad)
    # fig.tight_layout()

    return fig, tens

def legends_only_last_subplot(fig, tens):
    """ Function makes sure legend is only plotted on the 
    last subplot of each row
    
    Parameters
    ----------
    fig : Figure
        figure with subplots
    tens : list
        list in the subplot shape that indicates the numbering of axes 
        for each subplot

    Returns
    -------
    fig : Figure
        figure with subplots
    """
    for mat in tens:
        flat_mat = [j for i in mat for j in i]
        handles, labels = [], []
        for i,ax in enumerate(fig.axes[flat_mat[0]:flat_mat[-1]+1]):
            if i+flat_mat[0] in mat[-1]:
                h,l=ax.get_legend_handles_labels()
                handles+=h
                labels+=l
                if i+flat_mat[0]==mat[-1][-1]:
                    ax.legend(handles, labels)
            else:
                if ax.get_legend() is not None:
                    ax.get_legend().remove()
    # fig.tight_layout()

    return fig

def labels_only_last_subplot(fig, tens):
    """ Function makes sure labels are only plotted on the 
    first and last subplot of each row depending on their 
    left/right y position
    
    Parameters
    ----------
    fig : Figure
        figure with subplots
    tens : list
        list in the subplot shape that indicates the numbering of axes 
        for each subplot

    Returns
    -------
    fig : Figure
        figure with subplots
    """
    for mat in tens:
        for row,i in enumerate(mat):
            for num_ax,j in enumerate(i):
                if row>0 and num_ax==0:
                    fig.axes[j].set_ylabel('')
                    fig.axes[j].set_yticklabels('')
                if row<len(mat)-1 and num_ax==1:
                    fig.axes[j].set_ylabel('')
                    fig.axes[j].set_yticklabels('')
    # fig.tight_layout()

    return fig

def set_common_ylims(fig, tens):
    """ Function makes sure that all y limits are common
    across a row of subplots, even for twinx axes
    
    Parameters
    ----------
    fig : Figure
        figure with subplots
    tens : list
        list in the subplot shape that indicates the numbering of axes 
        for each subplot

    Returns
    -------
    fig : Figure
        figure with subplots
    """
    for mat in tens:
        for j in range(np.array(mat).shape[1]):
            y_min_all = np.min([lim for i,lim in enumerate(list((np.array([list(ax.get_ylim()) for ax in fig.axes]).T)[0])) if i in [m[j] for m in mat]])
            y_max_all = np.max([lim for i,lim in enumerate(list((np.array([list(ax.get_ylim()) for ax in fig.axes]).T)[1])) if i in [m[j] for m in mat]])
            for m in mat:
                fig.axes[m[j]].set_ylim(y_min_all,y_max_all)
    # fig.tight_layout()

    return fig

def add_column_titles(fig, tens, list_sites):
    """ Function adds column titles
    
    Parameters
    ----------
    fig : Figure
        figure with subplots
    tens : list
        list in the subplot shape that indicates the numbering of axes 
        for each subplot
    list_sites : list
        List of sites, 1 site per column
        will be used to label each column

    Returns
    -------
    fig : Figure
        figure with subplots
    """
    for ax, col in zip([fig.axes[m[0]] for m in tens[0]], list_sites):
        ax.set_title(col,fontdict={'fontsize': 20})
    # fig.tight_layout()

    return fig

def align_ylabels(fig, tens):
    """ Function aligns all left and right y labels
    
    Parameters
    ----------
    fig : Figure
        figure with subplots
    tens : list
        list in the subplot shape that indicates the numbering of axes 
        for each subplot

    Returns
    -------
    fig : Figure
        figure with subplots
    """
    fig.align_ylabels([fig.axes[m[0][0]] for m in tens])
    fig.align_ylabels([fig.axes[m[-1][-1]] for m in tens])
    # fig.tight_layout()

    return fig

def plot_same_new_figure(old_fig, new_ax_og):
    """ Function takes a Figure object and replots it identically

    Parameters
    ----------
    old_ax : matplotlib.axes._axes.Axes
        Axis of the original figure
    new_ax : matplotlib.axes._axes.Axes
        Axis of the new figure
    """
    for old_ax in old_fig.axes:
        new_ax = sharing_axis(new_ax_og, old_fig, old_ax)
        # recover_figsize(old_fig)

        # Re-plot Line2D objects
        recover_Line2D(old_ax, new_ax)

        # Recover axhline (horizontal lines)
        recover_axhline(old_ax, new_ax)

        # Re-plot fill_between (PolyCollection) objects
        recover_fill_between(old_ax, new_ax)

        # Recover axis labels and title from the original axes
        # Recover tick labels (if any custom ticks were used)
        # Recover x and y limits from the original axes
        recover_axis_formatting(old_ax, new_ax)

        # Recover legend (if present)
        recover_legend(old_ax, new_ax)

        recover_axis_position(old_ax, new_ax)
