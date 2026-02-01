@echo off
cd /d "%~dp0.."
echo Building Index...
python indexing/index_manager.py
pause
