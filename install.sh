
# apt
sudo apt install -y python3-venv
sudo apt install libatlas3-base  # for numpy
sudo apt-get install python3-numpy 

# Matplotlib
# ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory
sudo apt-get install libopenjp2-7

# pigiod
sudo apt-get -y install pigpio python3-pigpio
sudo pigpiod

# Python venv
python3 -m venv --system-site-packages venv 
source venv/bin/activate

pip install -e .
pip install -r requirements.txt