#!/usr/bin/env python3

'''Make Cozmo behave like a Braitenberg machine with virtual light sensors and wheels as actuators.

The following is the starter code for lab.
'''

import asyncio
import time
import cozmo

def braitenberg_machine(robot: cozmo.robot.Robot):
    '''The core of the braitenberg machine program'''

    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

    print("Press CTRL-C to quit")
    
    while True:
       # Sense the current brightness values on the right and left
       sensor_right = sense_brightness(rows=[1:10])
       sensor_left = sense_brightness(rows=[10:20])
       
       # Map the sensors to actuators
       # TODO: you might want to switch which sensor is mapped to which motor
       motor_right = mapping_funtion(sensor_left)
       motor_left = mapping_funtion(sensor_right)
       
       # Send commands to the robot
       robot.drive_wheels(motor_right, motor_left)

       time.sleep(.1)


cozmo.run_program(braitenberg_machine, use_viewer=True, force_viewer_on_top=True)
