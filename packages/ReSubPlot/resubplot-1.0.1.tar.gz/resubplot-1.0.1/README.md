# ReSubPlot

**ReSubPlot** (Replot figures to SubPlots): Plot one or many existing figure objects into a subplots() and manage
labels, titles, legends, alignments, etc.
On top of this, the package can also be used to extract the legend from a Python Figure object and plot the
figure and the label in two independent PDF files.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **ReSubPlot** (find the PyPi page here: https://pypi.org/project/ReSubPlot/).

```bash
pip install ReSubPlot
```

Install all the required packages (dependencies) from the *requirements.txt*  file.


```bash
pip install -r requirements.txt
```

Place *requirements.txt* in the directory where you plan to run the command. If the file is in a different directory, specify its path, for example, *path/to/requirements.txt*.

## Usage

### Command line

The package can be used directly on the command line with the built-in CLI, by calling one of **master** or **legend**

#### Master plot

```bash
ReSubPlot master -f config_master.toml
```

When using the package this way, all the information is stored in the TOML file *config_master.toml*. It should respect
the following structure:

```
# Configuration file for ReSubPlot.master_plot_from_toml

[pickle]
# path to the pickle where the list of list of Figure objects is saved
path = 'list_figs.pkl'

[sites]
# list of sites (string), there will be a column per site in the subplot result
list = ['Moosehide', 'Rockcreek', 'Sunnydale']

[pad]
# float that controls the padding between subplots, we suggest 0.03
pad  = 0.03

[save]
# Whether or not to save the master plot to a pdf
# If True: pass the name of the created pdf (e.g. path = 'master_plot')
# If False: pass None (path = None)
path = 'master_plot'
```

Importantly, the user needs to have saved all figures they want to have plotted on the master plot
in a specific format in a pickle. The format of the pickle is a list of list of Python Figure objects.
The list of lists should be in a *(m * n)* shape, e.g.

```
[[fig_1_1, ..., fig_1_n],
 [fig_2_1, ..., fig_2_n],
 ...
 [fig_m_1, ..., fig_m_n]]
```
The list of sites parameter should be a list of *n* string entries, one for each column of the master plot.

The output is a master plot with *n* columns (one per site), and *m* rows (one per type of plot). 

#### Legend on and off

The second functionality of **ReSubPlot** is to strip the legend off of a Python figure. This can also be
done from the command line, by calling
```bash
ReSubPlot legend -f config_legend.toml
```

When using the package this way, all the information is stored in the TOML file *config_master.toml*. It should respect
the following structure:

```
# Configuration file for ReSubPlot.isolate_legend_from_toml

[pickle]
# path to the pickle where the Figure objects is saved
path = 'figure.pkl'


[save]
# Whether or not to save the master plot to a pdf
# If True: pass the name of the created pdf (e.g. path = 'master_plot')
# If False: pass None (path = None)
path = 'my_cool_figure'
```

This is straightforward, the pickle should be a figure object. It will then create 3 PDF plots:
- a plot with the legend (the original plot)
- the same plot without the legend
- a figure that only shows the legend and nothing else

### Direct use of functions in Python 

#### Master plot

The CLI **master** call corresponds to the function **master_plot_from_toml()**, hence, the equivalent call
to what was described earlier is
```
from ReSubPlot.master_toml import master_plot_from_toml
master_plot_from_toml(config_toml_path)
```

Now, if the user has a list of list of figures (or matrix, in the shape *(m * n)*) called **mat_fig**,
and a list of sites of length n (each entry is a string) called **list_sites**, then, the function
master_plot() can be called directly in the following way

```
from ReSubPlot.plotting_funcs import master_plot
fig, tens = master_plot(mat_fig, list_sites)
```

The function will return:
-  **fig**: the master plot figure, a Python figure object
- **tens**: a list of list of list... the outermost shape is *(m * n)*, and each element is itself a list of integers which label the axis for a particular subplot *(i,j)*. The *(i,j)* element of **tens** can be [17,18] for instance, and this means that the 17th and 18th axes of the figure are found in subplot *(i,j)* (in the case of a twinx() axis for instance).

#### Legend on and off

The CLI **legend** call corresponds to the function **isolate_legend_from_toml()**, hence, the equivalent call
to what was described earlier is
```
from ReSubPlot.master_toml import isolate_legend_from_toml
isolate_legend_from_toml(config_toml_path)
```

Now, if the user has a figure (it is here called fig_no_legend) object in their python notebook, they can directly apply the function to it
```
from ReSubPlot.legends import isolate_legend
fig_with_legend, fig_no_legend, legend = isolate_legend(fig_no_legend, plot_name)
```
and it will return three objects:
- fig_with_legend is the original figure with the legend (we called it as fig_no_legend)
- fig_no_legend is now the original figure without the legend
- legend is the matplotlib legend object

Furthermore, 3 PDFs have been created.

## Examples

The user can find some inspiration on how to use **ReSubPlot** by looking at the examples provided.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
