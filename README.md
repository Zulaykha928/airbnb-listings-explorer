# Airbnb Listings Explorer

A Python command-line application for exploring and analyzing Airbnb listing data using pandas and Plotly.

## Features

- Load and clean Airbnb listing data from CSV
- Display dataset summary information
- Search listings by column and value
- Calculate average prices using grouped aggregation
- Export selected columns to a new CSV file
- Generate price distribution visualizations
- Generate neighbourhood listing visualizations
- Log application activity and errors
- Automated tests with pytest

## Project Structure

airbnb-listings-explorer/
- data/
  - raw/ - original Airbnb dataset
  - processed/ - exported data
  - plots/ - generated visualizations
- src/
  - data_handler.py - data loading, cleaning, searching, and aggregation
  - visualization.py - Plotly visualizations
  - cli.py - command-line output logic
- tests/ - automated tests
- main.py - application entry point
- requirements.txt - Python dependencies
- setup.sh - setup script

## Setup

Run:

```bash
chmod +x setup.sh
./setup.sh