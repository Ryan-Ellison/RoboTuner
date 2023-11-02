from Motor import Motor
import time

motor = Motor()
motor.led_G()
motor.home()
time.sleep(0.5)
motor.led_B()
time.sleep(0.5)
motor.led_Off()
motor.deinit()
