#!/bin/bash
cd "$(dirname "$0")/.."

if command -v python3 &>/dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

echo "Running Evaluation Pipeline..."
$PYTHON evaluation/evaluation_pipeline.py
