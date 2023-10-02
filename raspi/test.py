import os
import termios
import sys
import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import keyboard

os.system("stty -echo")

kit = MotorKit(i2c=board.I2C())
stepper_style = stepper.MICROSTEP
current_step = 0

def print_step(x):
	print(f"current step: {current_step}")

keyboard.on_release_key('w', print_step)
keyboard.on_release_key('s', print_step)

while True:
	if keyboard.is_pressed('w'):
		current_step = kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper_style)
		
	elif keyboard.is_pressed('s'):
		current_step = kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper_style)
		
	elif keyboard.is_pressed('a') and stepper_style != stepper.MICROSTEP:
		stepper_style = stepper.MICROSTEP
		print("microstepping...")
		
	elif keyboard.is_pressed('d') and stepper_style != stepper.DOUBLE:
		stepper_style = stepper.DOUBLE
		print("doubling...")
		
	elif keyboard.is_pressed('esc'):
		break
		
	else:
		kit.stepper1.release()

os.system("stty echo")
termios.tcflush(sys.stdin, termios.TCIOFLUSH)
