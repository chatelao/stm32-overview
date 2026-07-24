#!/usr/bin/env bash
set -euo pipefail

echo "Installing application dependencies..."
pip install --upgrade pip
pip install pyyaml pydantic click
