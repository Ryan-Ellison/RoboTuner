from Motor import Motor
from Display import Display
import time

display = Display()
display.update_display("RoboTuner\nbooting up...")
time.sleep(2)
motor = Motor()
display.homing()
motor.set_led((0, 1, 0))
motor.set_speed(500)
motor.set_accel(1000)
motor.home()
time.sleep(0.5)
motor.set_led((0, 0, 1))
time.sleep(0.5)
motor.set_led((0, 0, 0))
motor.deinit(False)
