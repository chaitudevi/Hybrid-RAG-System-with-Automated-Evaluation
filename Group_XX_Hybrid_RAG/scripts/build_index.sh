#!/bin/bash
# Navigate to project root if script is run from scripts/
cd "$(dirname "$0")/.."

# Check if python is available
if command -v python3 &>/dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

echo "Building Index..."
$PYTHON indexing/index_manager.py
