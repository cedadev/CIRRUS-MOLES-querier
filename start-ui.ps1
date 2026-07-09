#!/usr/bin/env pwsh

# Sets up the environment
. .\setup-env.ps1

$ENV_FILE = "src\.env"

# Check if CHAINLIT_AUTH_SECRET exists in the .env
if ((Test-Path $ENV_FILE) -and (Select-String -Path $ENV_FILE -Pattern "CHAINLIT_AUTH_SECRET" -Quiet)) {
    Write-Host "Skipping key creation (already exists)"
}
else {
    # If not, creates the file and populates it
    Write-Host "Generating Chainlit key into .env"

    # Get only the second line of output from chainlit create-secret
    $secret = (chainlit create-secret | Select-Object -Index 1)

    if (!(Test-Path $ENV_FILE)) {
        New-Item -ItemType File -Path $ENV_FILE -Force | Out-Null
    }

    Add-Content -Path $ENV_FILE -Value $secret
}

# Changing path for the db to run properly
Set-Location src

# Check if SQLite database exists
$DB_FILE = "graphical_interface\chainlit.db"

if (Test-Path $DB_FILE) {
    Write-Host "Skipping DB creation (already exists)"
}
else {
    # If not, run the db creation file
    Write-Host "Creating Chainlit database"

    if (Test-Path "graphical_interface\init_sqlite_db.py") {
        python graphical_interface\init_sqlite_db.py
    }
}

# Start the UI
Write-Host "Starting Chainlit server"

# Set PYTHONPATH for this session
$env:PYTHONPATH = (Get-Location).Path

chainlit run graphical_interface\chainlit_chatbot.py -w