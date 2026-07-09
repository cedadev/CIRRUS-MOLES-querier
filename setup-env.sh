#!/bin/bash

# Creates the venv if it doesn't exist
if [ ! -d "CIRRUS_venv" ]; then
    # Must be python 3.12 or 3.13 for requirements to run (not checked here)
    echo "Creating virtual environment..."
    python3 -m venv CIRRUS_venv
else
    echo "Virtual environment already exists. Skipping creation."
fi

# Activates the venv
source CIRRUS_venv/bin/activate

# Upgrade pip and install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt