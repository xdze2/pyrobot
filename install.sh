
# apt
sudo apt install -y python3-venv
sudo apt install libatlas3-base  # for numpy

# pigiod
sudo apt-get -y install pigpio python3-pigpio
sudo pigpiod

python3 -m venv --system-site-packages venv 
source venv/bin/activate

pip install -e .

pip install -r requirements.txt