#!/usr/bin/env python3

'''Make Cozmo behave like a Braitenberg machine with virtual light sensors and wheels as actuators.

The following is the starter code for lab.
'''

import asyncio
import time
import cozmo
import cv2
import numpy as np
import sys


def sense_brightness(image, columns):
	'''Maps a sensor reading to a wheel motor command'''
	## TODO: Test that this function works and decide on the number of columns to use

	h = image.shape[0]
	w = image.shape[1]
	avg_brightness = 0

	for y in range(0, h):
		for x in columns:
			avg_brightness += image[y,x]

	avg_brightness /= (h*columns.shape[0])

	return avg_brightness

def mapping_funtion(sensor_value):
	'''Maps a sensor reading to a wheel motor command'''
	## TODO: Define the mapping to obtain different behaviors.
	motor_value = 0.1*sensor_value
	return motor_value

async def braitenberg_machine(robot: cozmo.robot.Robot):
	'''The core of the braitenberg machine program'''
	# Move lift down and tilt the head up
	robot.move_lift(-3)
	robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
	print("Press CTRL-C to quit")

	while True:
		
		#get camera image
		event = await robot.world.wait_for(cozmo.camera.EvtNewRawCameraImage, timeout=30)

		#convert camera image to opencv format
		opencv_image = cv2.cvtColor(np.asarray(event.image), cv2.COLOR_RGB2GRAY)
		# Determine the w/h of the new image
		h = opencv_image.shape[0]
		w = opencv_image.shape[1]
		sensor_n_columns = 20

		# Sense the current brightness values on the right and left of the image.
		sensor_right = sense_brightness(opencv_image, columns=np.arange(sensor_n_columns))
		sensor_left = sense_brightness(opencv_image, columns=np.arange(w-sensor_n_columns, w))

		print("sensor_right: " + str(sensor_right))
		print("sensor_left: " + str(sensor_left))

		# Map the sensors to actuators
		## TODO: You might want to switch which sensor is mapped to which motor.
		motor_right = mapping_funtion(sensor_left)
		motor_left = mapping_funtion(sensor_right)

		print("motor_right: " + str(motor_right))
		print("motor_left: " + str(motor_left))

		# Send commands to the robot
		await robot.drive_wheels(motor_right, motor_left)

		time.sleep(.1)


cozmo.run_program(braitenberg_machine, use_viewer=True, force_viewer_on_top=True)
