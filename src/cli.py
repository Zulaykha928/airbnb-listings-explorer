"""Command-line output and coordination logic."""


class CLI:
    """Provide user-friendly output for Airbnb Explorer operations."""

    def __init__(self, data_handler, visualization):
        """Store DataHandler and Visualization objects."""
        self.data_handler = data_handler
        self.visualization = visualization

    def display_summary(self):
        """Print dataset summary information."""
        summary = self.data_handler.get_summary()

        print("\n=== DATASET SUMMARY ===")
        print(f"Rows: {summary['row_count']}")
        print(f"Columns: {', '.join(summary['columns'])}")
        print("\nMissing values:")
        for column, count in summary["missing_values"].items():
            print(f"  {column}: {count}")

    def search_entries(self, column, value):
        """Search listings and print matching results."""
        results = self.data_handler.search_entries(column, value)

        print(f"\n=== SEARCH RESULTS ({len(results)}) ===")
        if not results:
            print("No matching listings found.")
            return

        for row in results[:20]:
            print(row)

        if len(results) > 20:
            print(f"\nShowing first 20 of {len(results)} results.")

    def export_data(self, output_file, columns):
        """Export selected columns and report the result."""
        path = self.data_handler.filter_and_export(
            output_file, columns
        )
        print(f"Data exported successfully to: {path}")

    def display_aggregate(self, column):
        """Print average prices grouped by a column."""
        results = self.data_handler.get_aggregate(column)

        print(f"\n=== AVERAGE PRICE BY {column.upper()} ===")
        for name, average in results.items():
            print(f"{name}: ${average:.2f}")

    def export_plot(self, plot_type):
        """Generate the requested plot and report success."""
        if plot_type == "price_dist":
            success = self.visualization.plot_price_distribution(
                self.data_handler.df
            )
        elif plot_type == "neighbourhood":
            success = self.visualization.plot_neighbourhood(
                self.data_handler.df
            )
        else:
            raise ValueError(f"Unknown plot type: {plot_type}")

        if success:
            print("Plot exported successfully to data/plots/")
        else:
            print("Plot could not be exported. Check the log for details.")