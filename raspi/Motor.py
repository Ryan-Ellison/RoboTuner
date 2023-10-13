import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)

kit2 = MotorKit(i2c=board.I2C(), steppers_microsteps=2)
kit4 = MotorKit(i2c=board.I2C(), steppers_microsteps=4)
kit8 = MotorKit(i2c=board.I2C(), steppers_microsteps=8)
kit16 = MotorKit(i2c=board.I2C(), steppers_microsteps=16)

stepper_style = stepper.MICROSTEP
current_step = 0

prev_tendency = 0
total_elapsed_time = 0


# move motor to push tuning slide out
def push():
	return kit4.stepper1.onestep(direction=stepper.FORWARD, style=stepper_style)
	
	
# move motor to pull tuning slide in
def pull():
	return kit4.stepper1.onestep(direction=stepper.BACKWARD, style=stepper_style)


# releases stepper motor in all kits to ensure it does not use power when it shouldn't
# all_but argument allows for a single exeption so one kit can continue running
def release_kits(all_but: int = -1):
	for i in range(4):
		if i != x:
			kits[i].stepper1.release()
			

# moves motor based on tendency (i.e. forward if tendecy > 1, backward if tendecty < -1)
# time_elapsed tells the motor how long to move based on how long it takes to get the tendencies
def move_from_tendency(tendency: float = 0, time_elapsed: float = 0):
	move_time = (time_elapsed - 0.025) * 1000
	
	if tendency > 5:
		for i in range(move_time):
			current_step = push()
			time.sleep(0.001)
		
	if tendency < -5:
		for i in range(move_time):
			current_step = pull()
			time.sleep(0.001)
			
	release_kits()
			

# moves the motor to the home position (currently this is whatever position it started in)
def move_home():
	if current_step > 0:
		while not (current_step < 5 and current_step > -5):
			current_step = pull()
			
	if current_step < 0:
		while not (current_step < 5 and current_step > -5):
			current_step = push()
			
	release_kits()
			
			
# moves the stepper motor up and down to signify its ready to play after powering on
def startup_move()
	for i in range(4):
		for j in range(50):
			current_step = push()
		
		for j in range(50):
			current_step = pull()
	
	release_kits()


# turns on LED if there is no movement (meaning high resistance) for a period of time
def resistence_check(tendency: float = 0, time_elapsed: float = 0,
						tend_threshold: float = 1, time_threshold: float = 2):
	if (tendency - prev_tendency) < tend_threshold:
		total_elapsed_time += time_elapsed
		
	if total_elapsed_time > time_threshold:
		GPIO.output(22, GPIO.HIGH)
	
	






