"""Plotly visualizations for Airbnb listing data."""

import logging
import os
import plotly.express as px

logger = logging.getLogger(__name__)


class Visualization:
    """Create and export Airbnb data visualizations."""

    def __init__(self, output_dir="data/plots"):
        """Create the output directory when necessary."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_price_distribution(self, df):
        """Create and save a histogram of listing prices."""
        try:
            if "price" not in df.columns:
                raise ValueError("Price column not found")

            plot_df = df.dropna(subset=["price"])
            plot_df = plot_df[plot_df["price"] > 0]

            fig = px.histogram(
                plot_df,
                x="price",
                nbins=50,
                title="Airbnb Price Distribution",
            )

            output_file = os.path.join(
                self.output_dir, "price_distribution.png"
            )
            fig.write_image(
                output_file,
                format="png",
                width=800,
                height=600,
            )
            logger.info("Saved plot to %s", output_file)
            return True

        except Exception as exc:
            logger.error("Plot error: %s", exc)
            return False

    def plot_neighbourhood(self, df):
        """Create and save a bar chart of listings by neighbourhood."""
        try:
            if "neighbourhood" not in df.columns:
                raise ValueError("Neighbourhood column not found")

            counts = (
                df["neighbourhood"]
                .fillna("Unknown")
                .value_counts()
                .head(20)
                .reset_index()
            )
            counts.columns = ["neighbourhood", "listings"]

            fig = px.bar(
                counts,
                x="neighbourhood",
                y="listings",
                title="Listings by Neighbourhood",
            )

            output_file = os.path.join(
                self.output_dir, "neighbourhood.png"
            )
            fig.write_image(
                output_file,
                format="png",
                width=1000,
                height=600,
            )
            logger.info("Saved plot to %s", output_file)
            return True

        except Exception as exc:
            logger.error("Plot error: %s", exc)
            return False