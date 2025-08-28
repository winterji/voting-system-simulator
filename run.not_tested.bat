@echo off
echo Initializing virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r req.txt

echo Starting GUI...
python src\gui_simulator.py

pause
