import argparse
import sys

from ReSubPlot.master_toml import master_plot_from_toml, isolate_legend_from_toml

# 1. Create new function that takes a TOML config file with path to pkl
# 2. Unpickle the figures
# 3. Link everything here

def main():
    # Create the parser
    mainparser = argparse.ArgumentParser(description="Call function master_plot_from_toml() or isolate_legend_from_toml()")
    # Add an argument
    subparsers = mainparser.add_subparsers(dest='command', required=True)

    master = subparsers.add_parser("master", help="Call function master_plot_from_toml")
    legend = subparsers.add_parser("legend", help="Call function isolate_legend_from_toml")

    for parser in [master, legend]:
        # it will be stored as dest='f'
        parser.add_argument("-f", "--configfile",
                            default=None, type=str, required=True, dest='f',
                            help="Path to ReSubPlot TOML configuration file.")

    master.set_defaults(func=master_plot_from_toml)
    legend.set_defaults(func=isolate_legend_from_toml)

    if len(sys.argv) == 1:
        mainparser.print_help(sys.stderr)
        sys.exit(1)

    else:
        args = mainparser.parse_args()
        if args.command == 'master':
            master_plot_from_toml(args.f)
        elif args.command == 'legend':
            isolate_legend_from_toml(args.f)
