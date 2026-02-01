@echo off
cd /d "%~dp0.."
echo Starting App...
streamlit run app/app.py
pause
