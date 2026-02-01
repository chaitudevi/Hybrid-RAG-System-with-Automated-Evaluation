@echo off
cd /d "%~dp0.."

echo Running Evaluation Pipeline...
python evaluation/evaluation_pipeline.py

echo.
echo Evaluation complete. Results saved in data/evaluation.
pause
