#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import perf_counter, sleep

steer_gear_ratio = 1/1 #ratio of steer motor speed over actual steering direction change
drive_gear_ratio = 1/1 #ratio of motor speed to wheel speed
sp_conv = 102.303 * drive_gear_ratio; #conversion factor from real car m/s to proportional robot deg/s

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
	print("Max right position:", max_right)
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
	print("Max left position:", max_left)
	return max_left

def align_center(max_left, max_right):
	steer_center=((max_right - max_left)/2.0)+1.5
	print("Steering center:", steer_center)
	steer_motor.run_to_rel_pos(position_sp=steer_center, speed_sp=700, stop_action="hold")


#Calculate the steering speed based on controller values
def calculate_steering_speed(s, i_s, s_dot):
	steering_speed = (kP*s + kD*s_dot)*steer_gear_ratio
	print(steering_speed)
	return steering_speed

#Calculate the change in robot speed based on IR sensor perceived distance
def calculate_speed_adjustment(speed, distance):
	return speed

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
kP = -4
kD = -10
kI = 0
s = 0
s_dot = 0

#SET ROBOT SPEED
motor_duty_cycle = 10*sp_conv #proportional real car m/s times conversion factor

#Set up general variables
previous_error = 0
current_error = 0
current_time = 0
previous_time = 0

start_time = perf_counter()

#Set up variables for control
start_time = perf_counter()
steer_speed = 0

previous_times = [start_time]*8
previous_8th_time = 0
index = 0
count = 0

left_sensor_value = left_color_sensor.value()
right_sensor_value = right_color_sensor.value()
current_s = (left_sensor_value-right_sensor_value)/20
previous_s = [current_s]*8
previous_8th_s = current_s

max_right = align_right()
max_left = align_left()
align_center(max_left, max_right)
steer_motor.wait_while('running')
steer_motor.stop(stop_action='brake')

#Control loop
while not touch_sensor.value():
        #Update environment variables
	current_time=perf_counter()
	left_sensor_value = left_color_sensor.value()
	right_sensor_value = right_color_sensor.value()

	#Update time
	current_time=perf_counter()
	
	#P control
	current_s = (left_sensor_value-right_sensor_value)/20

        #D control
	index = count%8
	previous_8th_s = previous_s[index]
	previous_s[index]=current_s
	previous_8th_time=previous_times[index]
	previous_times[index]=current_time
	s_dot = (s-previous_8th_s)/(current_time-previous_8th_time)

	count+=1
	
        #Use variables to adjust steering angle
	if(abs(current_s) <= 1):
		print("nothing")
		#steer_speed = 0
	else:
		steer_speed = calculate_steering_speed(current_s, 0, s_dot)
		steer_motor.run_forever(speed_sp=steer_speed)

        #Update motor speed
	left_motor.run_forever(speed_sp=motor_duty_cycle)
	right_motor.run_forever(speed_sp=motor_duty_cycle)

#Stop motor function before exiting
left_motor.stop(stop_action="brake")
right_motor.stop(stop_action="brake")
steer_motor.stop(stop_action="brake")
print("Exited successfully.")
