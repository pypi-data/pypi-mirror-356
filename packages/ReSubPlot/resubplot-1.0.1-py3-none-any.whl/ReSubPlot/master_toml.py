"""This module allows the user to plot the master plot from a TOML configuration
file dircetion from the command line."""

import pickle
import toml

from ReSubPlot.plotting_funcs import master_plot
from ReSubPlot.legends import isolate_legend

def master_plot_from_toml(config_toml_path):
    """Plot all figures on a common subplot grid from a TOML configuration file.

    Parameters
    ----------
    config_toml_path: str
        path to the TOML configuration file

    Returns
    -------
    pdf of the mater plot
    """

    with open(config_toml_path, 'r', encoding="utf-8") as f:
        config = toml.load(f)

    path_pkl = config['pickle']['path']
    list_sites = config['sites']['list']
    pad = config['pad']['pad']
    path_pdf = config['save']['path']

    with open(path_pkl, 'rb') as file:
        # Call load method to deserialize
        mat_fig = pickle.load(file)

    _,_ = master_plot(mat_fig, list_sites, pad=pad, save_plots=path_pdf)

def isolate_legend_from_toml(config_toml_path):
    """Plot all figures on a common subplot grid from a TOML configuration file.

    Parameters
    ----------
    config_toml_path: str
        path to the TOML configuration file

    Returns
    -------
    pdf of the mater plot
    """

    with open(config_toml_path, 'r', encoding="utf-8") as f:
        config = toml.load(f)

    path_pkl = config['pickle']['path']
    path_pdf = config['save']['path']

    with open(path_pkl, 'rb') as file:
        # Call load method to deserialize
        fig = pickle.load(file)

    _,_,_ = isolate_legend(fig, save_plots=path_pdf)
