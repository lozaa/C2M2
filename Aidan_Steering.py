#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import perf_counter, sleep

#Find max right of steering motor
def align_right():
	steer_previous = steer_motor.position
	print("Initial position:", steer_previous)
	steer_current = 0
	while True:
		steer_previous = steer_motor.position
		steer_motor.run_to_rel_pos(position_sp=-10, speed_sp=700)
		sleep(0.05)
		steer_current = steer_motor.position
		if((steer_current - steer_previous)>-5):
			max_right = steer_previous
			break
	return max_right

def align_left():
	steer_previous = steer_motor.position
	print("Initial position from right:", steer_previous)
	steer_current = 0
	while True:
		steer_previous = steer_motor.position
		steer_motor.run_to_rel_pos(position_sp=10, speed_sp=700)
		sleep(0.05)
		steer_current = steer_motor.position
		if((steer_current - steer_previous)<5):
			max_left = steer_previous
			break
	return max_left

def align_center(max_left, max_right):
	steer_center=((max_right - max_left)/2.0)-1.5
	print("Steering center:", steer_center)
	steer_motor.run_to_rel_pos(position_sp=steer_center, speed_sp=700, stop_action="hold")


#Calculate the steering angle based on controller values
def calculate_steering_angle(error, integral, derivative):
	return 0

#Calculate the change in robot speed based on IR sensor perceived distance
def calculate_speed_adjustment(speed, distance):
	return 0


#Connect motors
steer_motor = MediumMotor('outB'); assert steer_motor.connected, "Connect the medium motor to port B."
left_motor = LargeMotor('outC'); assert left_motor.connected, "Connect the left motor to port C."
right_motor = LargeMotor('outA'); assert right_motor.connected, "Connect the right motor to port A."

#Connect sensors
touch_sensor = TouchSensor()
right_color_sensor = ColorSensor('in2')
right_color_sensor.mode = 'COL-REFLECT'
left_color_sensor = ColorSensor('in1')
left_color_sensor.mode = 'COL-REFLECT'
ir_sensor = InfraredSensor('in3')

#Set up controller variables
kP = 1/25
kD = 0
kI = 0

#Set up general variables
previous_error = 0
current_error = 0
current_time = 0
previous_time = 0

start_time = perf_counter()

#Set up variables for D control
previous_values = [0]*8
previous_times = [start_time]*8
previous_index = 0
current_index = 0
count = 0

max_right = align_right()
max_left = align_left()
align_center(max_left, max_right)
steer_motor.wait_while('running')
steer_motor.stop(stop_action='brake')

#Control loop
while not touch_sensor.value():
	print("placeholder")

#Stop motor function before exiting
left_motor.stop(stop_action="brake")
right_motor.stop(stop_action="brake")
steer_motor.stop(stop_action="brake")
print("Exited successfully.")
