#!/bin/bash

set -e

echo "Setting up Airbnb Listings Explorer..."

python3 -m pip install -r requirements.txt

mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/plots

echo "Setup complete."
echo "Place listings.csv inside data/raw/"
echo "Then run: python3 main.py summary"