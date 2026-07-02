#!/usr/bin/env pwsh

# Creates the venv if it doesn't exist
if (-not (Test-Path "CIRRUS_venv")) {
    Write-Host "Creating virtual environment..."
    if (Get-Command py -ErrorAction SilentlyContinue) {
        if (py -3.13 --version 2>$null) {
            py -3.13 -m venv CIRRUS_venv
        }
        elseif (py -3.12 --version 2>$null) {
            py -3.12 -m venv CIRRUS_venv
        }
        else {
            Write-Error "Python 3.12 or 3.13 is required. Please install it from https://python.org."
            exit 1
        }
    }
    else {
        Write-Error "Python Launcher (py.exe) not found."
        exit 1
    }
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