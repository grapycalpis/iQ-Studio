#!/bin/bash

# Copyright (c) 2025 Innodisk Corp.
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# This script handles the installation of iqs-launcher.

# Exit on error and print commands.
set -ex

# --- Variables ---
# Project root directory.
ROOT="$(dirname "$(readlink -f "$0")")"
# System-wide installation path for the command.
INSTALL_PATH="/usr/local/bin"
# Path for the Python virtual environment.
PYTHON_VENV="$ROOT/iqs-venv"

# --- Setup ---
# Create and activate Python virtual environment.
mkdir -p "$PYTHON_VENV" || echo "venv directory already exists."
python3 -m venv "$PYTHON_VENV"
source "$PYTHON_VENV/bin/activate"

# --- Install ---
# Link the launcher script to the install path to make it a global command.
ln -sf "$ROOT/iqs-launcher.sh" "$INSTALL_PATH/iqs-launcher"

# Make scripts executable.
chmod +x "$ROOT/iqs-launcher.sh"
chmod +x "$ROOT/launcher.py"
