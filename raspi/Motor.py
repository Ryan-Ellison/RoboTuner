from TMC_2209.TMC_2209_StepperDriver import *
import time
import RPi.GPIO as GPIO

class Motor:
	tmc = None
	max_dist = 100
	max_accel = 1000
	max_speed = 250

	def __init__(_, max_dist=100, speed=250, accel=1000, en_pin=21, step_pin=16, dir_pin=20, stall_pin=26, ms_res=2):
		_.max_dist = max_dist
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
		_.tmc.set_stallguard_callback(26, 50, _.stall_callback, 500)
		_.tmc.set_motor_enabled(True)
		_.tmc.set_acceleration(_.max_accel)
		_.tmc.set_max_speed(_.max_speed)
		_.tmc.set_current_position(0)
		
		_.pins = {
			"r": 5,
			"g": 6,
			"b": 13
		}
		GPIO.setmode(GPIO.BCM)
		for color, pin in _.pins.items():
			GPIO.setup(pin, GPIO.OUT)
		_.led_Off()
		
	def deinit(_):
		_.tmc.set_motor_enabled(False)
		for color, pin in _.pins.items():
			GPIO.cleanup(pin)

	def mm_to_steps(self, mm):
		return int(mm/0.04*_.ms_res*0.95)
		
	def steps_to_mm(self_, steps):
		return steps/0.95/_.ms_res*0.04

	def home(_):
		_.tmc.run_to_position_steps(_.mm_to_steps(-_.max_dist))

	def stall_callback(_, channel):
		if (_.tmc.get_stallguard_result() != 0):
			print("StallGuard!	:	", _.tmc.get_stallguard_result())
			_.tmc.stop(stop_mode=StopMode.HARDSTOP)
			_.led_R()
			
	def push(_, dist=1):
		if (_.steps_to_mm(_.tmc.get_current_position()) + dist < _.max_dist):
			_.tmc.run_to_position_steps(_.mm_to_steps(dist))
		else:
			_.tmc.run_to_position_steps(_.mm_to_steps(_.max_dist), MovementAbsRel.ABSOLUTE)
			
	def pull(_, dist=1):
		if (_.steps_to_mm(_.tmc.get_current_position()) - dist > 0):
			_.tmc.run_to_position_steps(_.mm_to_steps(-dist))
		else:
			_.tmc.run_to_position_steps(0, MovementAbsRel.ABSOLUTE)
			
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
		
	def led_R(_):
		GPIO.output(_.pins["r"], GPIO.HIGH)
		GPIO.output(_.pins["g"], GPIO.LOW)
		GPIO.output(_.pins["b"], GPIO.LOW)
		
	def led_G(_):
		GPIO.output(_.pins["r"], GPIO.LOW)
		GPIO.output(_.pins["g"], GPIO.HIGH)
		GPIO.output(_.pins["b"], GPIO.LOW)
		
	def led_B(_):
		GPIO.output(_.pins["r"], GPIO.LOW)
		GPIO.output(_.pins["g"], GPIO.LOW)
		GPIO.output(_.pins["b"], GPIO.HIGH)
		
	def led_Off(_):
		GPIO.output(_.pins["r"], GPIO.LOW)
		GPIO.output(_.pins["g"], GPIO.LOW)
		GPIO.output(_.pins["b"], GPIO.LOW)
