'''
def main():
    print("Welcome to the Airbnb Listings Explorer!")


if __name__ == "__main__":
    main()
'''

"""Airbnb Listings Explorer command-line application."""

import argparse
import logging
import os

from src.data_handler import DataHandler
from src.visualization import Visualization
from src.cli import CLI


def build_parser():
    """Create and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Explore and analyze Airbnb listing data."
    )

    parser.add_argument(
        "--file",
        default="data/raw/listings.csv",
        help="Path to the Airbnb listings CSV file",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "summary",
        help="Display a summary of the dataset",
    )

    search_parser = subparsers.add_parser(
        "search",
        help="Search entries by column and value",
    )
    search_parser.add_argument("--column", required=True)
    search_parser.add_argument("--value", required=True)

    export_parser = subparsers.add_parser(
        "export",
        help="Export selected columns to CSV",
    )
    export_parser.add_argument("--output", required=True)
    export_parser.add_argument(
        "--columns",
        nargs="+",
        required=True,
    )

    aggregate_parser = subparsers.add_parser(
        "aggregate",
        help="Calculate average price grouped by a column",
    )
    aggregate_parser.add_argument("--column", required=True)

    plot_parser = subparsers.add_parser(
        "plot",
        help="Create and export a visualization",
    )
    plot_parser.add_argument(
        "--type",
        choices=["price_dist", "neighbourhood"],
        required=True,
    )

    return parser


def main():
    """Run the Airbnb Listings Explorer CLI."""
    logging.basicConfig(
        filename="airbnb_explorer.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    parser = build_parser()
    args = parser.parse_args()

    if not os.path.exists(args.file):
        parser.error(
            f"Dataset not found: {args.file}. "
            "Place listings.csv in data/raw/ or use --file."
        )

    try:
        handler = DataHandler(args.file)
        visualization = Visualization()
        cli = CLI(handler, visualization)

        if args.command == "summary":
            cli.display_summary()

        elif args.command == "search":
            cli.search_entries(args.column, args.value)

        elif args.command == "export":
            cli.export_data(args.output, args.columns)

        elif args.command == "aggregate":
            cli.display_aggregate(args.column)

        elif args.command == "plot":
            cli.export_plot(args.type)

    except (ValueError, FileNotFoundError) as exc:
        logging.error("Application error: %s", exc)
        parser.error(str(exc))


if __name__ == "__main__":
    main()