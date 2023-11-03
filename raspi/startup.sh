#! /bin/sh

#echo "connect 1A:06:B7:DA:2B:78\n" | bluetoothctl
#sleep 5
#echo "quit\n" | bluetoothctl
sudo python3 /home/pi/RoboTuner/raspi/Home_Motor.py
sudo python3 /home/pi/RoboTuner/raspi/Controller.py
