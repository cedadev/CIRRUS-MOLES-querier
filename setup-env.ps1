#!/bin/bash

# Creates the venv if it doesn't exist
if (-not (Test-Path "CIRRUS_venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv CIRRUS_venv
}
else {
    Write-Host "Virtual environment already exists. Skipping creation."
}

# Allow script execution for this session (Windows PowerShell)
Set-ExecutionPolicy RemoteSigned -Scope Process -Force

# Activate venv
& ".\CIRRUS_venv\Scripts\Activate.ps1"

# Upgrade pip and install dependencies
Write-Host "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt