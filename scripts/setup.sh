#!/bin/bash
set -e

# Create and activate virtual environment with uv
echo "Creating virtual environment..."
uv venv

# Activate the virtual environment
# Note: source doesn't work in regular scripts, so we'll instruct users
echo "Please activate the virtual environment:"
echo "source .venv/bin/activate"
echo "Then run this script again"

# Check if we're in a virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Virtual environment is not activated. Please activate it first:"
    echo "source .venv/bin/activate"
    exit 1
fi

# Install dependencies using uv
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Install Ansible dependencies
echo "Installing Ansible dependencies..."
ansible-galaxy install -r ansible/requirements.yml --roles-path .galaxy/roles
ansible-galaxy collection install -r ansible/requirements.yml --collections-path .galaxy/collections

echo "Development environment setup complete!"
