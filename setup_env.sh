#!/bin/bash

# Ensure Python 3.11 is installed and active
echo "Ensuring Python 3.11 is active..."
if ! command -v python3.11 &>/dev/null; then
    echo "Python 3.11 is not installed. Please install Python 3.11."
    exit 1
fi

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv .venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install required dependencies with --upgrade to ensure they are up-to-date
echo "Installing/upgrading dependencies from requirements.txt..."
pip install --upgrade -r requirements.txt

# Set up pre-commit hooks if .pre-commit-config.yaml exists
if [ -f ".pre-commit-config.yaml" ]; then
    echo "Installing pre-commit hooks..."
    pip install pre-commit
    pre-commit install
fi

echo "Environment setup is complete!"
