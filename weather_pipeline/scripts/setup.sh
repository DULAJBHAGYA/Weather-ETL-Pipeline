#!/bin/bash

# Weather ETL Pipeline Setup Script

echo "Setting up Weather ETL Pipeline..."

# Create necessary directories
echo "Creating directories..."
mkdir -p ../db
mkdir -p ../logs
mkdir -p ../docs

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ../venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source ../venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r ../requirements.txt

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "Creating .env file from template..."
    cp ../.env.template ../.env
    echo "Please edit ../.env and add your OpenWeatherMap API key"
fi

echo "Setup complete!"
echo "Next steps:"
echo "1. Edit ../.env and add your OpenWeatherMap API key"
echo "2. Run 'source ../venv/bin/activate' to activate the virtual environment"
echo "3. Run 'python -m src.main run' to execute the pipeline once"