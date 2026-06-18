#!/bin/bash

# Creates the venv if it doesn't exist
if [ ! -d "CIRRUS_venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv CIRRUS_venv
else
    echo "Virtual environment already exists. Skipping creation."
fi

# Activates the venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\CIRRUS_venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt