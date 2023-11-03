from Motor import Motor
import time

motor = Motor()
motor.set_led((0, 1, 0))
motor.set_speed(250)
motor.set_accel(500)
motor.home()
time.sleep(0.5)
motor.set_led((0, 0, 1))
time.sleep(0.5)
motor.set_led((0, 0, 0))
motor.deinit(False)
