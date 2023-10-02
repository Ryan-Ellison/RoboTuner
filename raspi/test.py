import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper


kit = MotorKit(i2c=board.I2C())

for i in range(200):
	kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
	
for i in range(200):
	kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

kit.stepper1.release()
