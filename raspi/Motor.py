from TMC_2209.TMC_2209_StepperDriver import *
import time
from gpiozero import RGBLED


class Motor:
	tmc = None
	
	def __init__(_, max_dist=100, min_dist=0, speed=2000, accel=1500, en_pin=21, step_pin=16, dir_pin=20, stall_pin=26, ms_res=2):
		_.max_dist = max_dist
		_.min_dist = min_dist
		_.max_accel = accel
		_.max_speed = speed
		_.ms_res = ms_res
		
		_.tmc = TMC_2209(en_pin, step_pin, dir_pin)
		_.tmc.set_movement_abs_rel(MovementAbsRel.RELATIVE)
		_.tmc.set_direction_reg(False)
		_.tmc.set_current(300)
		_.tmc.set_interpolation(True)
		_.tmc.set_spreadcycle(False)
		_.tmc.set_microstepping_resolution(ms_res)
		_.tmc.set_internal_rsense(False)
		#_.tmc.set_stallguard_callback(26, 50, _.stall_callback, 500)
		_.tmc.set_motor_enabled(True)
		_.tmc.set_acceleration(_.max_accel)
		_.tmc.set_max_speed(_.max_speed)
		_.tmc.set_current_position(0)
		
		_.led = RGBLED(5, 6, 13)
		
		_.tmc.run_to_position_steps_threaded(1)
		
	def deinit(_, complete=True):
		_.tmc.set_motor_enabled(False)
		if complete:
			_.tmc.deinit()

	def mm_to_steps(_, mm):
		return int(mm/0.04*_.ms_res*0.95)
		
	def steps_to_mm(_, steps):
		return steps/0.95/_.ms_res*0.04

	def home(_):
		_.tmc.run_to_position_steps(_.mm_to_steps(-_.max_dist))
		time.sleep(0.1)
		_.tmc.run_to_position_steps(_.mm_to_steps(1))

	def stall_callback(_, channel):
		if (_.tmc.get_stallguard_result() != 0):
			print("StallGuard!	:	", _.tmc.get_stallguard_result())
			_.tmc.stop(stop_mode=StopMode.HARDSTOP)
			_.set_led((1, 0, 0))
			
	def push(_, dist=1, wait=False):
		prev_color = _.led.value
		_.set_led((1, 1, 0))
		_.stop()
		_.wait()
		if (_.steps_to_mm(_.tmc.get_current_position()) + dist < _.max_dist):
			_.tmc.run_to_position_steps_threaded(_.mm_to_steps(dist))
		else:
			_.tmc.run_to_position_steps_threaded(_.mm_to_steps(_.max_dist), MovementAbsRel.ABSOLUTE)
		if wait:
			_.wait()
		_.set_led(prev_color)
		print("push", _.steps_to_mm(_.tmc.get_current_position()))
			
	def pull(_, dist=1, wait=False):
		prev_color = _.led.value
		_.set_led((0, 1, 1))
		_.stop()
		_.wait()
		if (_.steps_to_mm(_.tmc.get_current_position()) - dist > _.min_dist):
			_.tmc.run_to_position_steps_threaded(_.mm_to_steps(-dist))
		else:
			_.tmc.run_to_position_steps_threaded(_.min_dist, MovementAbsRel.ABSOLUTE)
		if wait:
			_.wait()
		_.set_led(prev_color)
		print("pull", _.steps_to_mm(_.tmc.get_current_position()))
			
	def wait(_):
		_.tmc.wait_for_movement_finished_threaded()
	
	def stop(_):
		_.tmc.stop(stop_mode=StopMode.HARDSTOP)
			
	def get_position(_):
		return (_.steps_to_mm(_.tmc.get_current_position()), _.tmc.get_current_position())
		
	def get_speed(_):
		return _.max_speed
		
	def set_speed(_, speed):
		_.max_speed = speed
		_.tmc.set_max_speed(_.max_speed)
		
	def get_accel(_):
		return _.max_accel
		
	def set_accel(_, accel):
		_.max_accel = accel
		_.tmc.set_acceleration(_.max_accel)
		
	def get_led(_):
		return _.led.value
		
	def set_led(_, rgb):
		_.led.color = (rgb[0], rgb[1], rgb[2])
		

