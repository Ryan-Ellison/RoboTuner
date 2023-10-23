from TMC_2209.TMC_2209_StepperDriver import *
import time

tmc = TMC_2209(21, 16, 20)

tmc.set_direction_reg(False)
tmc.set_current(1300)
tmc.set_interpolation(True)
tmc.set_spreadcycle(False)
tmc.set_microstepping_resolution(2)
tmc.set_internal_rsense(False)

tmc.set_acceleration(2000)
tmc.set_max_speed(1000)


def callback(_):
	print("StallGuard!")
	tmc.stop(stop_mode=StopMode.HARDSTOP)
	
tmc.set_stallguard_callback(19, 1, callback, 1)


tmc.set_motor_enabled(True)
tmc.run_to_position_steps(10, MovementAbsRel.RELATIVE)

success = tmc.run_to_position_steps(10000, MovementAbsRel.RELATIVE)
time.sleep(2)
success = tmc.run_to_position_steps(-10000, MovementAbsRel.RELATIVE)

print(tmc.get_steps_per_revolution())

tmc.set_motor_enabled(False)
