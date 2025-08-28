echo "Initializing virtual environment..."
python3 -m venv venv
echo "Activating virtual environment..."
source venv/bin/activate
echo "Installing dependencies..."
pip install -r req.txt
echo "Starting GUI..."
python3 src/gui_simulator.py