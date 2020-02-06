#!/usr/bin/env python3
from ev3dev.ev3 import *

touch_sensor = TouchSensor()
right_color_sensor = ColorSensor('in2')
right_color_sensor.mode = 'COL-REFLECT'
left_color_sensor = ColorSensor('in1')
left_color_sensor.mode = 'COL-REFLECT'

while True:
    if touch_sensor.value():
        print("right =", right_color_sensor.value())
        print("left =", left_color_sensor.value())
        sleep(0.5)
    
