# Get_Stats

sudo apt update
sudo apt install python3
python3 --version
sudo apt install python3-pip
pip3 --version
sudo apt install python3-venv

python3 -m venv pythonenv
source pythonenv/bin/activate

pip install flask psutil

To deactivate the virtual environment:
deactivate

pip freeze > requirements.txt
pip install -r requirements.txt

python python_app.py 

verify metrics:
JSON can be accessed through: http://<your-local-IP>:5000/stats
IP address can be found using ifconfig on Linux/macOS.
make sure port 5000 is open in your firewall settings

