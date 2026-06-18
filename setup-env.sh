#!/bin/bash

# Creates the venv if it doesn't exist
if [ ! -d "CIRRUS_venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv CIRRUS_venv
else
    echo "Virtual environment already exists. Skipping creation."
fi

# Activates the venv based on the OS type
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Windows machine detected."
    source CIRRUS_venv/Scripts/activate
else
    echo "Unix-like machine detected (macOS/Linux)."
    source CIRRUS_venv/bin/activate
fi

# Upgrade pip and install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt