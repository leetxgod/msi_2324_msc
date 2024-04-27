#/bin/zsh

echo "Activating the virtual env..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r ./requirements.txt

echo "Done!\nRun \"source .venv/bin/activate\" to enter the virtual environment!"
