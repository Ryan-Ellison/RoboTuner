import os
import termios
import sys
import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import keyboard
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(22, GPIO.OUT)

os.system("stty -echo")

kit2 = MotorKit(i2c=board.I2C(), steppers_microsteps=2)
kit4 = MotorKit(i2c=board.I2C(), steppers_microsteps=4)
kit8 = MotorKit(i2c=board.I2C(), steppers_microsteps=8)
kit16 = MotorKit(i2c=board.I2C(), steppers_microsteps=16)
kits = [kit2, kit4, kit8, kit16]
current_kit = 0

stepper_style = stepper.DOUBLE
current_step = 0
prev_step = 0
step_mm_conv = 0.02
kit_mm_conv = [1, 2, 4, 8]

def print_step(x):
	print(f"current step: {current_step},	current dist: {(current_step-prev_step)*0.02/kit_mm_conv[current_kit]}mm")
	
def release_kits(x):
	for i in range(4):
		if i != x:
			kits[i].stepper1.release()
			
#def led_off(x):
#	GPIO.output(22, GPIO.LOW)
#	GPIO.cleanup()

#keyboard.on_release_key('w', print_step)
#keyboard.on_release_key('s', print_step)
#keyboard.on_release_key('l', led_off)

while True:
	if keyboard.is_pressed('1'):
		current_kit = 0
		release_kits(0)
		
	if keyboard.is_pressed('2'):
		current_kit = 1
		release_kits(1)
		
	if keyboard.is_pressed('3'):
		current_kit = 2
		release_kits(2)
		
	if keyboard.is_pressed('4'):
		current_kit = 3
		release_kits(3)
		
	#if keyboard.is_pressed('l'):
		#GPIO.output(22, GPIO.HIGH)
		
	if keyboard.is_pressed('w'):
		prev_step = current_step
		#for i in range(1000):
		current_step = kits[current_kit].stepper1.onestep(direction=stepper.FORWARD, style=stepper_style)
		time.sleep(0.001)
		#print_step(None)
		
	elif keyboard.is_pressed('s'):
		prev_step = current_step
		#for i in range(1000):
		current_step = kits[current_kit].stepper1.onestep(direction=stepper.BACKWARD, style=stepper_style)
		time.sleep(0.001)
		#print_step(None)
		
	elif keyboard.is_pressed('a') and stepper_style != stepper.MICROSTEP:
		stepper_style = stepper.MICROSTEP
		print("microstepping...")
		
	elif keyboard.is_pressed('d') and stepper_style != stepper.DOUBLE:
		stepper_style = stepper.DOUBLE
		print("doubling...")
		
	elif keyboard.is_pressed('esc'):
		break
		
	else:
		release_kits(-1)

os.system("stty echo")
termios.tcflush(sys.stdin, termios.TCIOFLUSH)
