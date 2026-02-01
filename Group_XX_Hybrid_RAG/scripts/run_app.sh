#!/bin/bash
cd "$(dirname "$0")/.."
echo "Starting App..."
streamlit run app/app.py
