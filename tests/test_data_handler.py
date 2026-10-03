"""Tests for the DataHandler class."""

import pandas as pd

from src.data_handler import DataHandler


def create_test_csv(tmp_path):
    """Create a small Airbnb CSV for testing."""
    file_path = tmp_path / "listings.csv"

    data = pd.DataFrame(
        {
            "name": ["Listing A", "Listing B", "Listing C"],
            "neighbourhood": ["Downtown", "Midtown", "Downtown"],
            "room_type": ["Entire home/apt", "Private room", "Private room"],
            "price": ["$100.00", "$80.00", "$120.00"],
        }
    )

    data.to_csv(file_path, index=False)
    return file_path


def test_get_summary(tmp_path):
    """Test dataset summary information."""
    file_path = create_test_csv(tmp_path)
    handler = DataHandler(file_path)

    summary = handler.get_summary()

    assert summary["row_count"] == 3
    assert "price" in summary["columns"]


def test_search_entries(tmp_path):
    """Test searching by neighbourhood."""
    file_path = create_test_csv(tmp_path)
    handler = DataHandler(file_path)

    results = handler.search_entries("neighbourhood", "Downtown")

    assert len(results) == 2


def test_get_aggregate(tmp_path):
    """Test average price aggregation."""
    file_path = create_test_csv(tmp_path)
    handler = DataHandler(file_path)

    results = handler.get_aggregate("room_type")

    assert "Private room" in results
    assert results["Private room"] == 100.00


def test_filter_and_export(tmp_path):
    """Test exporting selected columns."""
    file_path = create_test_csv(tmp_path)
    handler = DataHandler(file_path)

    output_file = tmp_path / "output.csv"
    handler.filter_and_export(
        output_file,
        ["name", "price"],
    )

    exported = pd.read_csv(output_file)

    assert list(exported.columns) == ["name", "price"]
    assert len(exported) == 3