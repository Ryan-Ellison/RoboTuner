# Rasberry Pi Setup

1. Follow "Installing Blinka on Raspberry Pi" on learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
	```
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get install python3-pip
	```
	```
	sudo reboot
	```
	```
	sudo pip3 install --upgrade setuptools
	```
	```
	cd ~
	sudo pip3 install --upgrade adafruit-python-shell
	wget https://raw.guthubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
	sudo python3 raspi-blinka.py
	```
2. Install MotorKit librrary by adafruit
	```
	sudo pip3 install adafruit-circuitpython-motorkit
	```
