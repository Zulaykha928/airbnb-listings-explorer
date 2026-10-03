
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class DataHandler:
    """Handle Airbnb listing data with pandas."""

    def __init__(self, file_path):
        """Store the CSV path and load the dataset."""
        self.file_path = file_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Load and clean the Airbnb dataset."""
        try:
            self.df = pd.read_csv(self.file_path, low_memory=False)
            logger.info("Loaded dataset with %s rows", len(self.df))

            # Clean price values such as "$1,250.00".
            if "price" in self.df.columns:
                self.df["price"] = (
                    self.df["price"]
                    .astype(str)
                    .str.replace("$", "", regex=False)
                    .str.replace(",", "", regex=False)
                )
                self.df["price"] = pd.to_numeric(
                    self.df["price"], errors="coerce"
                )

                # Fill missing prices with the median.
                median_price = self.df["price"].median()
                self.df["price"] = self.df["price"].fillna(median_price)

                # Remove extreme price outliers using the IQR method.
                q1 = self.df["price"].quantile(0.25)
                q3 = self.df["price"].quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                self.df = self.df[
                    self.df["price"].between(lower, upper)
                ]

            # Handle missing neighbourhood values.
            if "neighbourhood" in self.df.columns:
                self.df["neighbourhood"] = self.df[
                    "neighbourhood"
                ].fillna("Unknown")

            return self.df

        except FileNotFoundError:
            logger.error("File %s not found", self.file_path)
            raise

    def get_summary(self):
        """Return row count, column names, and missing-value counts."""
        return {
            "row_count": len(self.df),
            "columns": self.df.columns.tolist(),
            "missing_values": self.df.isnull().sum().to_dict(),
        }

    def search_entries(self, column, value):
        """Return rows whose selected column matches the search value."""
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")

        matches = self.df[
            self.df[column].astype(str).str.contains(
                str(value), case=False, na=False
            )
        ]
        return matches.to_dict(orient="records")

    def filter_and_export(self, output_file, columns):
        """Export selected columns to a CSV file."""
        missing = [column for column in columns if column not in self.df.columns]
        if missing:
            raise ValueError(f"Columns not found: {missing}")

        self.df[columns].to_csv(output_file, index=False)
        logger.info("Exported data to %s", output_file)
        return output_file

    def get_aggregate(self, column):
        """Return average price grouped by the selected column."""
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")
        if "price" not in self.df.columns:
            raise ValueError("Price column not found")

        result = (
            self.df.groupby(column)["price"]
            .mean()
            .round(2)
            .sort_values(ascending=False)
        )
        return result.to_dict()