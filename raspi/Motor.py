from TMC_2209.TMC_2209_StepperDriver import *
import time

tmc = TMC_2209(21, 16, 20)

tmc.set_direction_reg(False)
tmc.set_current(300)
tmc.set_interpolation(True)
tmc.set_spreadcycle(False)
tmc.set_microstepping_resolution(2)
tmc.set_internal_rsense(False)

max_speed = 1000

tmc.set_acceleration(1000)
tmc.set_max_speed(max_speed)

def stall_callback(_):
	'''if tmc.get_stallguard_result() == 0:
		return'''
	print("StallGuard!	:	", tmc.get_stallguard_result())
	tmc.stop(stop_mode=StopMode.HARDSTOP)
	tmc.set_motor_enabled(False)
	tmc.set_motor_enabled(True)
	
def home():
	tmc.set_max_speed(500)
	tmc.run_to_position_steps(-100000, MovementAbsRel.RELATIVE)
	tmc.set_current_position(0)
	tmc.set_max_speed(max_speed)
	
#make steps to linear dist func
	
tmc.set_stallguard_callback(26, 55, stall_callback, 500)

tmc.set_motor_enabled(True)

home()
time.sleep(1)
#tmc.run_to_position_steps(10, MovementAbsRel.RELATIVE)
tmc.run_to_position_steps(2000, MovementAbsRel.RELATIVE)
time.sleep(1)
tmc.run_to_position_steps(-1500, MovementAbsRel.RELATIVE)

tmc.set_motor_enabled(False)
