#!/bin/bash

source ./setup-env.sh

ENV_FILE="src/.env"

# Check if CHAINLIT_AUTH_SECRET exists in the .env
if [ -f "$ENV_FILE" ] && grep -q "CHAINLIT_AUTH_SECRET" "$ENV_FILE"; then
    echo "Skipping key creation (already exists)"
else
    echo "Generating chainlit key into env"
    (chainlit create-secret | sed -n '2p') >> "$ENV_FILE"
fi

cd src

# Check if SQLite database exists
DB_FILE="graphical_interface/chainlit.db"
if [ -f "$DB_FILE" ]; then
    echo "Skipping DB creation (already exists)"
else
    echo "Creating chainlit database"
    if [ -f "graphical_interface/init_sqlite_db.py" ]; then
        python graphical_interface/init_sqlite_db.py
    fi
fi

# Start the UI
echo "Starting chainlit server"
export PYTHONPATH=$PWD
# Check if the flag is --JASMIN
if [ "$1" == "--JASMIN" ]; then
    echo "Running JASMIN UI"
    chainlit run graphical_interface/chainlit_chatbot.py -w --host 0.0.0.0 --port 8000
else
    chainlit run graphical_interface/chainlit_chatbot.py -w
fi