"""Tests for the Visualization class."""

import pandas as pd

from src.visualization import Visualization


def test_plot_price_distribution(tmp_path):
    """Test that the price distribution plot is created."""
    df = pd.DataFrame(
        {
            "price": [50, 75, 100, 125, 150],
        }
    )

    visualization = Visualization(output_dir=str(tmp_path))

    result = visualization.plot_price_distribution(df)

    assert result is True
    assert (tmp_path / "price_distribution.png").exists()


def test_plot_neighbourhood(tmp_path):
    """Test that the neighbourhood plot is created."""
    df = pd.DataFrame(
        {
            "neighbourhood": [
                "Downtown",
                "Downtown",
                "Midtown",
                "Uptown",
            ]
        }
    )

    visualization = Visualization(output_dir=str(tmp_path))

    result = visualization.plot_neighbourhood(df)

    assert result is True
    assert (tmp_path / "neighbourhood.png").exists()