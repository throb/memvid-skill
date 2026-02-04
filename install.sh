#!/bin/bash
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install dependencies
source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete. Memory index will be rebuilt on first run or manually via 'python3 scripts/rebuild.py'"
